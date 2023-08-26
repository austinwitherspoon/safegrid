import inspect
import sys
import types
from copy import deepcopy
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)
import typing

import pydantic
import shotgun_api3
import shotgun_api3.lib.mockgun
from typing_extensions import ClassVar, Literal, Self, get_args, get_origin


class GenericEntity(pydantic.BaseModel, extra="allow"):
    id: int
    type: str


from .fields import Filter, FilterGroup, ShotgunType, UnknownFieldType  # noqa: E402

# Type hint for shotgun instance
Shotgun = Union[shotgun_api3.Shotgun, shotgun_api3.lib.mockgun.Shotgun]
# Shotgun instance or a function that can generate one
# (useful for lazy loading connection)
Shotgun_or_builder = Union[Shotgun, Callable[[], Shotgun]]

# Default shotgun to use if none provided
DEFAULT_SHOTGUN: Optional[Shotgun_or_builder] = None


class SafegridException(Exception):
    pass


def swap_annotations(type_hint: Type) -> Tuple[Type, Optional[Type[ShotgunType]]]:
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
            fixed_arg, _found_sg_field = swap_annotations(arg)
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
                    if sys.version_info >= (3, 9):
                        if origin in [types.UnionType]:
                            new_type = Union[tuple(new_args)]  # type:ignore
                        else:
                            raise
                    else:
                        if origin in [typing.Union]:
                            new_type = Union[tuple(new_args)]
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


class EntityMeta(type(pydantic.BaseModel)):
    def __new__(
        mcs,
        cls_name: str,
        bases: Tuple[Type[Any], ...],
        namespace: Dict[str, Any],
        *args,
        **kwargs,
    ):
        _sg_fields = {}
        for base in bases:
            if hasattr(base, "_sg_fields"):
                _sg_fields.update(getattr(base, "_sg_fields"))
        annotations = namespace.get("__annotations__", {})
        for name, field_type in annotations.items():
            fixed_annotation, sg_field = swap_annotations(field_type)
            annotations[name] = fixed_annotation
            if sg_field:
                _sg_fields[name] = sg_field(name, None)  # type:ignore

        new_class = type(pydantic.BaseModel).__new__(
            mcs, cls_name, bases, namespace, *args, **kwargs
        )

        for name, field_info in new_class.model_fields.items():
            if name not in _sg_fields:
                _sg_fields[name] = UnknownFieldType(name, field_info)
            else:
                _sg_fields[name].field_info = field_info

        new_class._sg_fields = _sg_fields
        return new_class

    def __getattr__(self, name):
        """HACK!
        Pydantic raises an exception if you define a field named the same thing as a
        class variable - but we want to intentionally do that so we can access
        metadata about fields from MyEntity.field_name.
        So we are allowing access to all fields as class vars ONLY
        if the caller isn't pydantic itself!"""
        try:
            return super().__getattr__(name)
        except AttributeError:
            if hasattr(self, "_sg_fields"):
                if name in self._sg_fields:
                    stack = inspect.stack()
                    frame = stack[1].frame
                    if frame.f_globals["__name__"] != "pydantic._internal._fields":
                        return self._sg_fields[name]
                raise


class BaseEntity(
    pydantic.BaseModel,
    **{"metaclass": EntityMeta, "extra": "allow", "validate_assignment": True},
):
    type: ClassVar[str]
    id: Optional[int] = None
    _sg: ClassVar[Optional[Shotgun_or_builder]] = None
    _sg_fields: ClassVar[Dict[str, ShotgunType]] = {}

    @classmethod
    def find(
        cls,
        *arg_filters: Union[Filter, FilterGroup],
        filters: Optional[List[Union[list, dict]]] = None,
        extra_fields: Optional[Iterable[str]] = None,
        order: Optional[List[Dict[str, str]]] = None,
        filter_operator: Optional[Union[Literal["all"], Literal["any"]]] = None,
        limit: int = 0,
        retired_only: bool = False,
        page: int = 0,
        include_archived_projects: bool = True,
        additional_filter_presets: Optional[List[Dict[str, str]]] = None,
        sg: Optional[Shotgun] = None,
        _cache: Optional[Dict[Type["BaseEntity"], Dict[int, "BaseEntity"]]] = None,
        **kwargs,
    ):
        sg_con = sg or cls.__get_shotgun__(f"finding {cls.type}")

        find_kwargs = {
            "order": order,
            "filter_operator": filter_operator,
            "limit": limit,
            "retired_only": retired_only,
            "page": page,
            "include_archived_projects": include_archived_projects,
            "additional_filter_presets": additional_filter_presets,
        }
        # HACK: To support mockgun which isn't identical to shotgun, we
        # only send kwargs that are in the signature of the find method
        find_kwargs = {
            key: value
            for key, value in find_kwargs.items()
            if key in inspect.signature(sg_con.find).parameters
        }

        filters_copy: List[Union[List, Dict]] = (
            deepcopy(filters) if filters else []  # type:ignore
        )

        filters_copy.extend([f.to_sg_filter() for f in arg_filters])
        filters_copy.extend(
            [field_name, "is", value] for field_name, value in kwargs.items()
        )
        if not filters_copy and filters is None:
            raise SafegridException("No filters provided!")

        raw_results: List[Dict[str, Any]] = sg_con.find(
            cls.type,
            filters=filters_copy,
            fields=list(cls.model_fields.keys()) + list((extra_fields or [])),
            **find_kwargs,
        )  # type:ignore

        _cache = _cache or {}
        if cls not in _cache:
            _cache[cls] = {}

        results: List[Self] = []
        for raw_sg_data in raw_results:
            model = cls.model_construct(set(raw_sg_data.keys()), **raw_sg_data)
            results.append(model)
            _cache[cls][model.id] = model  # type:ignore

        cls._hydrate_nested_fields(results, _cache, sg_con)  # type:ignore
        [i.__init__(**i.__dict__) for i in results]

        return results

    @classmethod
    def _nested_model_fields(cls) -> Dict[str, Tuple[Type["BaseEntity"]]]:
        """Returns a dictionary of all fields that are nested models.
        For example, if you Version model has `entity:Shot`, where
        we need to also download data for the Shot model when we download
        Versions."""
        nested_fields = {}
        for field_name, field in cls._sg_fields.items():
            annotation = field.field_info.annotation
            all_possible_types = get_all_valid_types(annotation)
            model_types = [
                possible_type
                for possible_type in all_possible_types
                if issubclass(possible_type, BaseEntity)
            ]
            if model_types:
                nested_fields[field_name] = tuple(model_types)
        return nested_fields

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @classmethod
    def _hydrate_nested_fields(
        cls,
        models: List[Self],
        _cache: Dict[Type["BaseEntity"], Dict[int, "BaseEntity"]],
        sg: Optional[Shotgun],
    ):
        _nested_model_fields = cls._nested_model_fields()

        # if there are no nested fields, we can skip the rest of this
        if not _nested_model_fields:
            return models

        # collect all the ids we need to fetch and construct empty models
        ids_to_fetch: Dict[Type["BaseEntity"], Set[int]] = {}
        new_models: Dict[Type["BaseEntity"], Dict[int, "BaseEntity"]] = {}

        for model in models:
            for field_name, nested_types in _nested_model_fields.items():
                if not model[field_name]:
                    continue
                is_list = isinstance(model[field_name], list)

                for i, item in enumerate(
                    model[field_name] if is_list else [model[field_name]]
                ):
                    sg_type = item.get("type")
                    matching_model_type = next(
                        (
                            model_type
                            for model_type in nested_types
                            if model_type.type == sg_type
                        ),
                        None,
                    )
                    if matching_model_type is None:
                        continue
                    cached_model = _cache.get(matching_model_type, {}).get(item["id"])
                    if cached_model:
                        if is_list:
                            model[field_name][i] = cached_model
                        else:
                            model[field_name] = cached_model
                        continue
                    if matching_model_type not in ids_to_fetch:
                        ids_to_fetch[matching_model_type] = set()
                    ids_to_fetch[matching_model_type].add(item["id"])
                    empty_model = matching_model_type.model_construct(
                        set(matching_model_type.model_fields.keys()), **item
                    )
                    if matching_model_type not in new_models:
                        new_models[matching_model_type] = {}
                    new_models[matching_model_type][item["id"]] = empty_model
                    if is_list:
                        model[field_name][i] = empty_model
                    else:
                        model[field_name] = empty_model

        # fetch all the data
        for model_type, ids in ids_to_fetch.items():
            results = model_type.find(
                filters=[["id", "in", list(ids)]],
                sg=sg,
                _cache=_cache,
            )
            if model_type not in _cache:
                _cache[model_type] = {}
            for result in results:
                matching_model = new_models[model_type][result.id]  # type:ignore
                matching_model.__dict__.update(result.__dict__)
                _cache[model_type][result.id] = matching_model  # type:ignore

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        # double check has type!
        if not hasattr(cls, "type") or not cls.type:
            raise SafegridException(
                f"Class '{cls}' must have a 'type' attribute defined!"
            )

    @pydantic.model_validator(mode="before")
    @classmethod
    def _validate_type(cls, data):
        if isinstance(data, dict):
            if data.get("type", cls.type) != cls.type:
                raise ValueError(
                    f"Invalid type {data.get('type')}, expected {cls.type}"
                )
        return data

    def get(self, name, default=None):
        return getattr(self, name, default)

    @classmethod
    def __get_shotgun__(cls, context: Optional[str] = None) -> Shotgun:
        global DEFAULT_SHOTGUN
        # is class level SG?
        if cls._sg is not None:
            if callable(cls._sg):
                cls._sg = cls._sg()
            return cls._sg
        # is there a global default sg?
        if DEFAULT_SHOTGUN is not None:
            if callable(DEFAULT_SHOTGUN):
                DEFAULT_SHOTGUN = DEFAULT_SHOTGUN()
            return DEFAULT_SHOTGUN
        message = "No shotgun instance provided!"
        if context:
            message = f"No shotgun instance provided while {context}!"
        raise SafegridException(message)


def set_default_shotgun(sg: Shotgun_or_builder):
    global DEFAULT_SHOTGUN
    DEFAULT_SHOTGUN = sg
