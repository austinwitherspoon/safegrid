import pydantic
from .exceptions import SafegridException


import inspect
import types
from typing import Optional, Tuple, Type, Union
from typing_extensions import ClassVar, get_args, get_origin


class GenericEntity(pydantic.BaseModel, extra="allow"):
    id: int
    type: str


from .fields import ShotgunType  # noqa


def remove_shotgun_types(type_hint: Type) -> Tuple[Type, Optional[Type[ShotgunType]]]:
    """Takes a type hint and attempts to see if there's a nested ShotgunType annotation.
    If so, swap it with it's inner _output_type, and return the both fields
    """
    origin = get_origin(type_hint)
    if origin == ClassVar:
        return type_hint, None
    if inspect.isclass(type_hint) and issubclass(type_hint, ShotgunType):
        return type_hint._output_type, type_hint
    if origin and inspect.isclass(origin) and issubclass(origin, ShotgunType):
        return get_args(type_hint)[0], origin

    # check if is a type with nested types
    if hasattr(type_hint, "__args__"):
        new_args = []
        sg_field = None
        for arg in get_args(type_hint):
            fixed_arg, _found_sg_field = remove_shotgun_types(arg)
            new_args.append(fixed_arg)
            if _found_sg_field:
                if sg_field is None:
                    sg_field = _found_sg_field
                else:
                    raise SafegridException("Multiple ShotgunType annotations found")
        if sg_field is not None:
            if origin:
                try:
                    new_type = origin[tuple(new_args)]  # type:ignore
                except TypeError:
                    # Only an issue in newer python versions, after they
                    # changed to UnionType instead of Union
                    if origin in [types.UnionType]:  # type:ignore
                        new_type = Union[tuple(new_args)]  # type:ignore
                    else:
                        raise
                return new_type, sg_field
            else:
                raise SafegridException(
                    "Unknown origin - Something went wrong processing type hints!"
                )
    return type_hint, None


def get_all_valid_types(type_hint: Type) -> Tuple[Type]:
    """Processes all nested types and returns a list of all
    possible variations of direct object types.
    For example, `Union[str, Optional[Union[List[str],List[int]]]]`
    would return `(str, None, List[str], List[int])`
    """
    origin = get_origin(type_hint)
    if origin == ClassVar:
        return (type_hint,)
    if origin and inspect.isclass(origin) and issubclass(origin, ShotgunType):
        return get_args(type_hint)
    if inspect.isclass(type_hint) and issubclass(type_hint, ShotgunType):
        return (type_hint._output_type,)
    if get_args(type_hint):
        new_args = []
        for arg in get_args(type_hint):
            new_args.extend(get_all_valid_types(arg))
        return tuple(new_args)
    return (type_hint,)
