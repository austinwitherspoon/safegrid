import safegrid
from shotgun_api3.lib import mockgun
import pytest


def test_sg_injection_methods(sg: mockgun.Shotgun):
    """Test the different ways we can pass shotgun to safegrid"""

    class Version(safegrid.BaseEntity):
        type = "Version"
        code: str

    # function that generates a shotgun instance
    sg_builder = lambda: sg  # noqa

    # reset the default shotgun instances
    safegrid.entity.DEFAULT_SHOTGUN = None
    Version._sg = None

    # Test passing a shotgun instance to the find method
    Version.find(filters=[], sg=sg)

    # it should fail if we don't pass a shotgun instance,
    # since there is no class level or global shotgun instances
    with pytest.raises(safegrid.SafegridException):
        Version.find(filters=[])

    # test setting default sg on model
    Version._sg = sg
    Version.find(filters=[])
    # test setting "builder" function on model
    Version._sg = sg_builder
    Version.find(filters=[])
    # reset
    Version._sg = None

    with pytest.raises(safegrid.SafegridException):
        Version.find(filters=[])

    # test setting default sg on safegrid
    safegrid.set_default_shotgun(sg)
    Version.find(filters=[])
    # test builder function
    safegrid.set_default_shotgun(sg_builder)
    Version.find(filters=[])

    # reset
    safegrid.entity.DEFAULT_SHOTGUN = None
