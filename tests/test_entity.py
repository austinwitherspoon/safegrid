from typing import List, Optional

import pydantic
import safegrid
from shotgun_api3.lib import mockgun
import pytest
import safegrid.exceptions
from safegrid.fields import (
    TextField,
    MultiEntityField,
    EntityField,
)


def test_sg_injection_methods(sg: mockgun.Shotgun):
    """Test the different ways we can pass shotgun to safegrid"""

    class Version(safegrid.BaseEntity):
        type = "Version"
        code: TextField

    # function that generates a shotgun instance
    sg_builder = lambda: sg  # noqa

    # reset the default shotgun instances
    safegrid.entity.DEFAULT_SHOTGUN = None
    Version._sg = None

    # Test passing a shotgun instance to the find method
    Version.find(filters=[], sg=sg)

    # it should fail if we don't pass a shotgun instance,
    # since there is no class level or global shotgun instances
    with pytest.raises(safegrid.exceptions.SafegridException):
        Version.find(filters=[])

    # test setting default sg on model
    Version._sg = sg
    Version.find(filters=[])
    # test setting "builder" function on model
    Version._sg = sg_builder
    Version.find(filters=[])
    # reset
    Version._sg = None

    with pytest.raises(safegrid.exceptions.SafegridException):
        Version.find(filters=[])

    # test setting default sg on safegrid
    safegrid.set_default_shotgun(sg)
    Version.find(filters=[])
    # test builder function
    safegrid.set_default_shotgun(sg_builder)
    Version.find(filters=[])

    # reset
    safegrid.entity.DEFAULT_SHOTGUN = None


def test_filtering(sg: mockgun.Shotgun):
    class Version(safegrid.BaseEntity):
        _sg = sg
        type = "Version"
        code: TextField
        entity: Optional[EntityField]

    # classic sg style filtering
    versions = Version.find(filters=[["entity", "is_not", None]])
    assert versions

    # Kwargs for equals filtering
    versions = Version.find(tags=None)
    assert versions

    # SQLAlchemy style class variable filters!
    versions = Version.find(Version.entity != None, Version.code.contains("bunny"))
    assert versions

    # all of the above
    versions = Version.find(
        Version.entity.type_is("Shot"),  # type: ignore
        Version.code.contains("bunny"),
        filters=[["entity", "is_not", None]],
    )


def test_entity_get_item(sg: mockgun.Shotgun):
    """You can interact with an entity as if it were a dictionary"""

    class Version(safegrid.BaseEntity):
        _sg = sg
        type = "Version"
        code: TextField

    version = next(iter(Version.find(filters=[])))

    name = version["code"]
    assert isinstance(name, str) and len(name) > 1
    name_get = version.get("code")
    assert name_get == name
    assert version.get("not_a_field") is None

    # you can also set values
    version["code"] = "new name"
    assert version.code == "new name"


def test_nested_models(sg: mockgun.Shotgun):
    """Test nested models"""

    class Shot(safegrid.BaseEntity):
        _sg = sg
        type = "Shot"
        code: TextField

    class Version(safegrid.BaseEntity):
        _sg = sg
        type = "Version"
        code: TextField
        entity: EntityField[Optional[Shot]]

    version = next(
        iter(Version.find(Version.entity != None, Version.entity.type_is("Shot")))
    )

    assert isinstance(version.entity, Shot)
    assert isinstance(version.entity.code, str)

    # Lets make an infinite loop, loading project with users and users with projects
    class Project(safegrid.BaseEntity):
        _sg = sg
        type = "Project"
        name: TextField
        users: MultiEntityField[List["User"]]  # type: ignore

    class User(safegrid.BaseEntity):
        _sg = sg
        type = "HumanUser"
        login: TextField
        projects: MultiEntityField[List[Project]]

    projects = Project.find(filters=[])

    # Lets confirm that it goes forever deep
    target = next(iter(p for p in projects if p.users))
    for _ in range(10):
        if isinstance(target, User):
            target = target.projects[0]
        elif isinstance(target, Project):
            target = target.users[0]


def test_bad_input(sg: mockgun.Shotgun):
    class Version(safegrid.BaseEntity):
        _sg = sg
        type = "Version"
        code: TextField

    with pytest.raises(pydantic.ValidationError):
        Version(
            code="test", type="Shot"  # type: ignore
        )  # Invalid type, expected "Version"!

    with pytest.raises(pydantic.ValidationError):
        # Validation error for type of code
        Version(code=1)  # type: ignore

    with pytest.raises(safegrid.SafegridException):
        # Class must have type attribute defined!
        class EntityWithoutTypeField(safegrid.BaseEntity):
            code: str

    with pytest.raises(safegrid.SafegridException):
        Version.find()  # No filters provided!
