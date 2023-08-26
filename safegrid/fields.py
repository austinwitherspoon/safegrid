from datetime import date, datetime, timedelta
from typing_extensions import Literal, Self, TypeVar, TypedDict
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from typing_extensions import (
    TYPE_CHECKING,
    Any,
    Generic,
    Iterable,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeAlias,
    Union,
    overload,
)
import typing
from .entity import GenericEntity
from enum import Enum


class FilterGroupOperator(Enum):
    Any = "any"
    All = "all"


class FilterOperator(Enum):
    Is = "is"
    IsNot = "is_not"
    LessThan = "less_than"
    GreaterThan = "greater_than"
    Contains = "contains"
    NotContains = "not_contains"
    StartsWith = "starts_with"
    EndsWith = "ends_with"
    Between = "between"
    InLast = "in_last"
    InNext = "in_next"
    In = "in"
    NotIn = "not_in"
    TypeIs = "type_is"
    TypeIsNot = "type_is_not"
    InCalendarDay = "in_calendar_day"
    InCalendarWeek = "in_calendar_week"
    InCalendarMonth = "in_calendar_month"
    NameContains = "name_contains"
    NameNotContains = "name_not_contains"
    NameStartsWith = "name_starts_with"
    NameEndsWith = "name_ends_with"


_T = TypeVar("_T")
_value_is = Optional[_T]
_value_is_not = Optional[_T]
_value_less_than = Optional[_T]
_value_greater_than = Optional[_T]
_value_contains = Optional[_T]
_value_not_contains = Optional[_T]
_value_starts_with: TypeAlias = _T
_value_ends_with: TypeAlias = _T
_value_between = Tuple[Optional[_T], Optional[_T]]
_value_in_last = Tuple[
    int,
    Union[
        Literal["HOUR"],
        Literal["DAY"],
        Literal["WEEK"],
        Literal["MONTH"],
        Literal["YEAR"],
    ],
]
_value_in_next = Tuple[
    int,
    Union[
        Literal["HOUR"],
        Literal["DAY"],
        Literal["WEEK"],
        Literal["MONTH"],
        Literal["YEAR"],
    ],
]
_value_in = Iterable[Optional[_T]]
_value_not_in = Iterable[Optional[_T]]
_value_type_is = Optional[_T]
_value_type_is_not = Optional[_T]
_value_in_calendar_day: TypeAlias = _T
_value_in_calendar_week: TypeAlias = _T
_value_in_calendar_month: TypeAlias = _T
_value_name_contains: TypeAlias = str
_value_name_not_contains: TypeAlias = str
_value_name_starts_with: TypeAlias = str
_value_name_ends_with: TypeAlias = str


FilterValue = TypeVar("FilterValue")


class Filter(Generic[FilterValue]):
    def __init__(self, field: str, operator: FilterOperator, value: FilterValue):
        self.field = field
        self.operator = operator
        self.value = value

    def __repr__(self) -> str:
        return f"Filter({self.to_sg_filter()})"

    def __str__(self) -> str:
        return self.__repr__()

    def to_sg_filter(self) -> list:
        if self.operator in [FilterOperator.InLast, FilterOperator.InNext]:
            return [self.field, self.operator.value] + list(self.value)  # type: ignore
        else:
            return [self.field, self.operator.value, self.value]

    if TYPE_CHECKING:

        @overload
        def __new__(
            cls, field: str, operator: Literal[FilterOperator.Is], value: _value_is
        ) -> "Filter"[_value_is]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.IsNot],
            value: _value_is_not,
        ) -> "Filter"[_value_is_not]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.LessThan],
            value: _value_less_than,
        ) -> "Filter"[_value_less_than]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.GreaterThan],
            value: _value_greater_than,
        ) -> "Filter"[_value_greater_than]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.Contains],
            value: _value_contains,
        ) -> "Filter"[_value_contains]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NotContains],
            value: _value_not_contains,
        ) -> "Filter"[_value_not_contains]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.StartsWith],
            value: _value_starts_with,
        ) -> "Filter"[_value_starts_with]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.EndsWith],
            value: _value_ends_with,
        ) -> "Filter"[_value_ends_with]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.Between],
            value: _value_between,
        ) -> "Filter"[_value_between]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.InLast],
            value: _value_in_last,
        ) -> "Filter"[_value_in_last]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.InNext],
            value: _value_in_next,
        ) -> "Filter"[_value_in_next]:
            ...

        @overload
        def __new__(
            cls, field: str, operator: Literal[FilterOperator.In], value: _value_in
        ) -> "Filter"[_value_in]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NotIn],
            value: _value_not_in,
        ) -> "Filter"[_value_not_in]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.TypeIs],
            value: _value_type_is,
        ) -> "Filter"[_value_type_is]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.TypeIsNot],
            value: _value_type_is_not,
        ) -> "Filter"[_value_type_is_not]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.InCalendarDay],
            value: _value_in_calendar_day,
        ) -> "Filter"[_value_in_calendar_day]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.InCalendarWeek],
            value: _value_in_calendar_week,
        ) -> "Filter"[_value_in_calendar_week]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.InCalendarMonth],
            value: _value_in_calendar_month,
        ) -> "Filter"[_value_in_calendar_month]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NameContains],
            value: _value_name_contains,
        ) -> "Filter"[_value_name_contains]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NameNotContains],
            value: _value_name_not_contains,
        ) -> "Filter"[_value_name_not_contains]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NameStartsWith],
            value: _value_name_starts_with,
        ) -> "Filter"[_value_name_starts_with]:
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NameEndsWith],
            value: _value_name_ends_with,
        ) -> "Filter"[_value_name_ends_with]:
            ...

        def __new__(
            cls,
            field: str,
            operator: FilterOperator,
            value: Any,
        ) -> "Filter":
            ...

    def __and__(self, other: Union["Filter", "FilterGroup"]) -> "FilterGroup":
        if isinstance(other, Filter):
            return FilterGroup(FilterGroupOperator.All, [self, other])
        elif isinstance(other, FilterGroup):
            if other.operator == FilterGroupOperator.All:
                return FilterGroup(FilterGroupOperator.All, [self, *other.filters])
            elif other.operator == FilterGroupOperator.Any:
                return FilterGroup(FilterGroupOperator.All, [self, other])
            else:
                raise ValueError(
                    f"Cannot add FilterGroup with operator {other.operator} to Filter"
                )
        else:
            raise TypeError(f"Cannot add {type(other)} to Filter")

    def __or__(self, other: Union["Filter", "FilterGroup"]) -> "FilterGroup":
        if isinstance(other, Filter):
            return FilterGroup(FilterGroupOperator.Any, [self, other])
        elif isinstance(other, FilterGroup):
            if other.operator == FilterGroupOperator.All:
                return FilterGroup(FilterGroupOperator.Any, [self, other])
            elif other.operator == FilterGroupOperator.Any:
                return FilterGroup(FilterGroupOperator.Any, [self, *other.filters])
            else:
                raise ValueError(
                    f"Cannot add FilterGroup with operator {other.operator} to Filter"
                )
        else:
            raise TypeError(f"Cannot add {type(other)} to Filter")

    def __add__(self, other: Union["Filter", "FilterGroup"]) -> "FilterGroup":
        return self.__and__(other)


class FilterGroup:
    def __init__(
        self,
        operator: FilterGroupOperator,
        filters: typing.List[Union[Filter, "FilterGroup"]],
    ):
        self.operator = operator
        self.filters = filters

    def __repr__(self) -> str:
        return f"FilterGroup({self.to_sg_filter()})"

    def __str__(self) -> str:
        return self.__repr__()

    def to_sg_filter(self) -> dict:
        return {
            "filter_operator": self.operator.value,
            "filters": [f.to_sg_filter() for f in self.filters],
        }

    def __and__(self, other: Union[Filter, "FilterGroup"]) -> "FilterGroup":
        if isinstance(other, Filter):
            if self.operator == FilterGroupOperator.All:
                return FilterGroup(FilterGroupOperator.All, [*self.filters, other])
            elif self.operator == FilterGroupOperator.Any:
                return FilterGroup(FilterGroupOperator.All, [self, other])
            else:
                raise ValueError(
                    f"Cannot add Filter with operator {other.operator} to FilterGroup"
                )
        elif isinstance(other, FilterGroup):
            if other.operator == FilterGroupOperator.All:
                return FilterGroup(
                    FilterGroupOperator.All, [*self.filters, *other.filters]
                )
            elif other.operator == FilterGroupOperator.Any:
                return FilterGroup(FilterGroupOperator.All, [*self.filters, other])
            else:
                raise ValueError(
                    f"Cannot add FilterGroup with operator {other.operator} to group"
                )
        else:
            raise TypeError(f"Cannot add {type(other)} to FilterGroup")

    def __or__(self, other: Union[Filter, "FilterGroup"]) -> "FilterGroup":
        if isinstance(other, Filter):
            if self.operator == FilterGroupOperator.All:
                return FilterGroup(FilterGroupOperator.Any, [self, other])
            elif self.operator == FilterGroupOperator.Any:
                return FilterGroup(FilterGroupOperator.Any, [*self.filters, other])
            else:
                raise ValueError(
                    f"Cannot add Filter with operator {other.operator} to FilterGroup"
                )
        elif isinstance(other, FilterGroup):
            if other.operator == FilterGroupOperator.All:
                return FilterGroup(FilterGroupOperator.Any, [self, other])
            elif other.operator == FilterGroupOperator.Any:
                return FilterGroup(
                    FilterGroupOperator.Any, [*self.filters, *other.filters]
                )
            else:
                raise ValueError(
                    f"Cannot add FilterGroup with operator {other.operator} to group"
                )
        else:
            raise TypeError(f"Cannot add {type(other)} to FilterGroup")

    def __add__(self, other: Union[Filter, "FilterGroup"]) -> "FilterGroup":
        return self.__and__(other)


class ShotgunType:
    _output_type = None
    _pydantic_schema = None

    def __init__(self, name: str, pydantic_field: FieldInfo):
        self._name = name
        self.field_info = pydantic_field

    @property
    def name(self) -> str:
        return self.field_info.alias or self._name

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> Any:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...

        def __set__(self, instance: Any, value: str) -> None:
            ...

        def __delete__(self, instance: Any) -> None:
            ...

    elif not typing.TYPE_CHECKING:

        def is_(self, __value: _value_is) -> Filter[_value_is]:
            return Filter(self.name, FilterOperator.Is, __value)

        def is_not(self, __value: _value_is_not) -> Filter[_value_is_not]:
            return Filter(self.name, FilterOperator.IsNot, __value)

        def less_than(self, __value: _value_less_than) -> Filter[_value_less_than]:
            return Filter(self.name, FilterOperator.LessThan, __value)

        def greater_than(
            self, __value: _value_greater_than
        ) -> Filter[_value_greater_than]:
            return Filter(self.name, FilterOperator.GreaterThan, __value)

        def contains(self, __value: _value_contains) -> Filter[_value_contains]:
            return Filter(self.name, FilterOperator.Contains, __value)

        def not_contains(
            self, __value: _value_not_contains
        ) -> Filter[_value_not_contains]:
            return Filter(self.name, FilterOperator.NotContains, __value)

        def starts_with(
            self, __value: _value_starts_with
        ) -> Filter[_value_starts_with]:
            return Filter(self.name, FilterOperator.StartsWith, __value)

        def ends_with(self, __value: _value_ends_with) -> Filter[_value_ends_with]:
            return Filter(self.name, FilterOperator.EndsWith, __value)

        def between(self, __value: _value_between) -> Filter[_value_between]:
            return Filter(self.name, FilterOperator.Between, __value)

        def in_last(self, __value: _value_in_last) -> Filter[_value_in_last]:
            return Filter(self.name, FilterOperator.InLast, __value)

        def in_next(self, __value: _value_in_next) -> Filter[_value_in_next]:
            return Filter(self.name, FilterOperator.InNext, __value)

        def in_(self, __value: _value_in) -> Filter[_value_in]:
            return Filter(self.name, FilterOperator.In, __value)

        def not_in(self, __value: _value_not_in) -> Filter[_value_not_in]:
            return Filter(self.name, FilterOperator.NotIn, __value)

        def type_is(self, __value: _value_type_is) -> Filter[_value_type_is]:
            return Filter(self.name, FilterOperator.TypeIs, __value)

        def type_is_not(
            self, __value: _value_type_is_not
        ) -> Filter[_value_type_is_not]:
            return Filter(self.name, FilterOperator.TypeIsNot, __value)

        def in_calendar_day(
            self, __value: _value_in_calendar_day
        ) -> Filter[_value_in_calendar_day]:
            return Filter(self.name, FilterOperator.InCalendarDay, __value)

        def in_calendar_week(
            self, __value: _value_in_calendar_week
        ) -> Filter[_value_in_calendar_week]:
            return Filter(self.name, FilterOperator.InCalendarWeek, __value)

        def in_calendar_month(
            self, __value: _value_in_calendar_month
        ) -> Filter[_value_in_calendar_month]:
            return Filter(self.name, FilterOperator.InCalendarMonth, __value)

        def name_contains(
            self, __value: _value_name_contains
        ) -> Filter[_value_name_contains]:
            return Filter(self.name, FilterOperator.NameContains, __value)

        def name_not_contains(
            self, __value: _value_name_not_contains
        ) -> Filter[_value_name_not_contains]:
            return Filter(self.name, FilterOperator.NameNotContains, __value)

        def name_starts_with(
            self, __value: _value_name_starts_with
        ) -> Filter[_value_name_starts_with]:
            return Filter(self.name, FilterOperator.NameStartsWith, __value)

        def name_ends_with(
            self, __value: _value_name_ends_with
        ) -> Filter[_value_name_ends_with]:
            return Filter(self.name, FilterOperator.NameEndsWith, __value)

        def __eq__(self, __value: _value_is) -> Filter[_value_is]:
            return self.is_(__value)

        def __ne__(self, __value: _value_is_not) -> Filter[_value_is_not]:
            return self.is_not(__value)

        def __lt__(self, __value: _value_less_than) -> Filter[_value_less_than]:
            return self.less_than(__value)

        def __gt__(self, __value: _value_greater_than) -> Filter[_value_greater_than]:
            return self.greater_than(__value)

        def __le__(self, __value):
            raise NotImplementedError(
                "Shotgrid does not currently have a 'less than or equal to' filter"
            )

        def __ge__(self, __value):
            raise NotImplementedError(
                "Shotgrid does not currently have a 'greater than or equal to' filter"
            )


class UnknownFieldType(ShotgunType):
    if typing.TYPE_CHECKING:

        def is_(self, __value: _value_is) -> Filter[_value_is]:
            ...

        def is_not(self, __value: _value_is_not) -> Filter[_value_is_not]:
            ...

        def less_than(self, __value: _value_less_than) -> Filter[_value_less_than]:
            ...

        def greater_than(
            self, __value: _value_greater_than
        ) -> Filter[_value_greater_than]:
            ...

        def contains(self, __value: _value_contains) -> Filter[_value_contains]:
            ...

        def not_contains(
            self, __value: _value_not_contains
        ) -> Filter[_value_not_contains]:
            ...

        def starts_with(
            self, __value: _value_starts_with
        ) -> Filter[_value_starts_with]:
            ...

        def ends_with(self, __value: _value_ends_with) -> Filter[_value_ends_with]:
            ...

        def between(self, __value: _value_between) -> Filter[_value_between]:
            ...

        def in_last(self, __value: _value_in_last) -> Filter[_value_in_last]:
            ...

        def in_next(self, __value: _value_in_next) -> Filter[_value_in_next]:
            ...

        def in_(self, __value: _value_in) -> Filter[_value_in]:
            ...

        def not_in(self, __value: _value_not_in) -> Filter[_value_not_in]:
            ...

        def type_is(self, __value: _value_type_is) -> Filter[_value_type_is]:
            ...

        def type_is_not(
            self, __value: _value_type_is_not
        ) -> Filter[_value_type_is_not]:
            ...

        def in_calendar_day(
            self, __value: _value_in_calendar_day
        ) -> Filter[_value_in_calendar_day]:
            ...

        def in_calendar_week(
            self, __value: _value_in_calendar_week
        ) -> Filter[_value_in_calendar_week]:
            ...

        def in_calendar_month(
            self, __value: _value_in_calendar_month
        ) -> Filter[_value_in_calendar_month]:
            ...

        def name_contains(
            self, __value: _value_name_contains
        ) -> Filter[_value_name_contains]:
            ...

        def name_not_contains(
            self, __value: _value_name_not_contains
        ) -> Filter[_value_name_not_contains]:
            ...

        def name_starts_with(
            self, __value: _value_name_starts_with
        ) -> Filter[_value_name_starts_with]:
            ...

        def name_ends_with(
            self, __value: _value_name_ends_with
        ) -> Filter[_value_name_ends_with]:
            ...

        def __eq__(self, __value: _value_is) -> Filter[_value_is]:
            ...

        def __ne__(self, __value: _value_is_not) -> Filter[_value_is_not]:
            ...

        def __lt__(self, __value: _value_less_than) -> Filter[_value_less_than]:
            ...

        def __gt__(self, __value: _value_greater_than) -> Filter[_value_greater_than]:
            ...

        def __le__(self, __value):
            raise NotImplementedError(
                "Shotgrid does not currently have a 'less than or equal to' filter"
            )

        def __ge__(self, __value):
            raise NotImplementedError(
                "Shotgrid does not currently have a 'greater than or equal to' filter"
            )


TextCastTo = TypeVar("TextCastTo", default=str)


class Text(ShotgunType, Generic[TextCastTo]):
    _output_type = str

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> TextCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...

        def is_(self, __value: _value_is[str]) -> Filter[_value_is[str]]:
            ...

        def is_not(self, __value: _value_is_not[str]) -> Filter[_value_is_not[str]]:
            ...

        def contains(
            self, __value: _value_contains[str]
        ) -> Filter[_value_contains[str]]:
            ...

        def not_contains(
            self, __value: _value_not_contains[str]
        ) -> Filter[_value_not_contains[str]]:
            ...

        def starts_with(
            self, __value: _value_starts_with[str]
        ) -> Filter[_value_starts_with[str]]:
            ...

        def ends_with(
            self, __value: _value_ends_with[str]
        ) -> Filter[_value_ends_with[str]]:
            ...

        def in_(self, __value: _value_in[str]) -> Filter[_value_in[str]]:
            ...

        def not_in(self, __value: _value_not_in[str]) -> Filter[_value_not_in[str]]:
            ...

        def __eq__(self, __value: _value_is[str]) -> Filter[_value_is[str]]:
            ...

        def __ne__(self, __value: _value_is_not[str]) -> Filter[_value_is_not[str]]:
            ...


FloatCastTo = TypeVar("FloatCastTo", default=float)


class Float(ShotgunType, Generic[FloatCastTo]):
    _output_type = float

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> FloatCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...

        def is_(self, __value: _value_is[float]) -> Filter[_value_is[float]]:
            ...

        def is_not(self, __value: _value_is_not[float]) -> Filter[_value_is_not[float]]:
            ...

        def less_than(
            self, __value: _value_less_than[float]
        ) -> Filter[_value_less_than[float]]:
            ...

        def greater_than(
            self, __value: _value_greater_than[float]
        ) -> Filter[_value_greater_than[float]]:
            ...

        def between(
            self, __value: _value_between[float]
        ) -> Filter[_value_between[float]]:
            ...

        def in_(self, __value: _value_in[float]) -> Filter[_value_in[float]]:
            ...

        def not_in(self, __value: _value_not_in[float]) -> Filter[_value_not_in[float]]:
            ...

        def __eq__(self, __value: _value_is[float]) -> Filter[_value_is[float]]:
            ...

        def __ne__(self, __value: _value_is_not[float]) -> Filter[_value_is_not[float]]:
            ...

        def __lt__(
            self, __value: _value_less_than[float]
        ) -> Filter[_value_less_than[float]]:
            ...

        def __gt__(
            self, __value: _value_greater_than[float]
        ) -> Filter[_value_greater_than[float]]:
            ...


class EntityProtocol(Protocol):
    type: str
    id: int


class EntityDict(TypedDict):
    type: str
    id: int


EntityObject = Union[EntityProtocol, EntityDict]
EntityType = Union[Type[BaseModel], str]

EntityCastTo = TypeVar("EntityCastTo", default=typing.List[GenericEntity])


class MultiEntity(ShotgunType, Generic[EntityCastTo]):
    _output_type = typing.List[GenericEntity]

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> EntityCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...

        def is_(
            self, __value: _value_is[EntityObject]
        ) -> Filter[_value_is[EntityObject]]:
            ...

        def is_not(
            self, __value: _value_is_not[EntityObject]
        ) -> Filter[_value_is_not[EntityObject]]:
            ...

        def in_(
            self, __value: _value_in[EntityObject]
        ) -> Filter[_value_in[EntityObject]]:
            ...

        def not_in(
            self, __value: _value_not_in[EntityObject]
        ) -> Filter[_value_not_in[EntityObject]]:
            ...

        def type_is(
            self, __value: _value_type_is[EntityType]
        ) -> Filter[_value_type_is[EntityType]]:
            ...

        def type_is_not(
            self, __value: _value_type_is_not[EntityType]
        ) -> Filter[_value_type_is_not[EntityType]]:
            ...

        def name_contains(
            self, __value: _value_name_contains
        ) -> Filter[_value_name_contains]:
            ...

        def name_not_contains(
            self, __value: _value_name_not_contains
        ) -> Filter[_value_name_not_contains]:
            ...

        def name_starts_with(
            self, __value: _value_name_starts_with
        ) -> Filter[_value_name_starts_with]:
            ...

        def name_ends_with(
            self, __value: _value_name_ends_with
        ) -> Filter[_value_name_ends_with]:
            ...

        def __eq__(
            self, __value: _value_is[EntityObject]
        ) -> Filter[_value_is[EntityObject]]:
            ...

        def __ne__(
            self, __value: _value_is_not[EntityObject]
        ) -> Filter[_value_is_not[EntityObject]]:
            ...


NumberCastTo = TypeVar("NumberCastTo", default=int)


class Number(ShotgunType, Generic[NumberCastTo]):
    _output_type = int

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> NumberCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...

        def is_(self, __value: _value_is[int]) -> Filter[_value_is[int]]:
            ...

        def is_not(self, __value: _value_is_not[int]) -> Filter[_value_is_not[int]]:
            ...

        def less_than(
            self, __value: _value_less_than[int]
        ) -> Filter[_value_less_than[int]]:
            ...

        def greater_than(
            self, __value: _value_greater_than[int]
        ) -> Filter[_value_greater_than[int]]:
            ...

        def between(self, __value: _value_between[int]) -> Filter[_value_between[int]]:
            ...

        def in_(self, __value: _value_in[int]) -> Filter[_value_in[int]]:
            ...

        def not_in(self, __value: _value_not_in[int]) -> Filter[_value_not_in[int]]:
            ...

        def __eq__(self, __value: _value_is[int]) -> Filter[_value_is[int]]:
            ...

        def __ne__(self, __value: _value_is_not[int]) -> Filter[_value_is_not[int]]:
            ...

        def __lt__(
            self, __value: _value_less_than[int]
        ) -> Filter[_value_less_than[int]]:
            ...

        def __gt__(
            self, __value: _value_greater_than[int]
        ) -> Filter[_value_greater_than[int]]:
            ...


class Addressing(MultiEntity, Generic[EntityCastTo]):
    pass


CheckboxCastTo = TypeVar("CheckboxCastTo", default=bool)


class Checkbox(ShotgunType, Generic[CheckboxCastTo]):
    _output_type = bool

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> CheckboxCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...

        def is_(self, __value: _value_is[bool]) -> Filter[_value_is[bool]]:
            ...

        def is_not(self, __value: _value_is_not[bool]) -> Filter[_value_is_not[bool]]:
            ...

        def __eq__(self, __value: _value_is[bool]) -> Filter[_value_is[bool]]:
            ...

        def __ne__(self, __value: _value_is_not[bool]) -> Filter[_value_is_not[bool]]:
            ...


class Color(Text, Generic[TextCastTo]):
    """Color field type in shotgrid.
    value:	str
    example:	255,0,0 | pipeline_step

    pipeline_step indicates the Task color inherits from the Pipeline Step color.
    """


class Currency(Float, Generic[FloatCastTo]):
    pass


DateCastTo = TypeVar("DateCastTo", default=date)


class Date(ShotgunType, Generic[DateCastTo]):
    _output_type = date

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> DateCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...

        def is_(
            self, __value: _value_is[Union[date, str]]
        ) -> Filter[_value_is[Union[date, str]]]:
            ...

        def is_not(
            self, __value: _value_is_not[Union[date, str]]
        ) -> Filter[_value_is_not[Union[date, str]]]:
            ...

        def less_than(
            self, __value: _value_less_than[Union[date, str]]
        ) -> Filter[_value_less_than[Union[date, str]]]:
            ...

        def greater_than(
            self, __value: _value_greater_than[Union[date, str]]
        ) -> Filter[_value_greater_than[Union[date, str]]]:
            ...

        def between(
            self, __value: _value_between[Union[date, str]]
        ) -> Filter[_value_between[Union[date, str]]]:
            ...

        def in_last(self, __value: _value_in_last) -> Filter[_value_in_last]:
            ...

        def in_next(self, __value: _value_in_next) -> Filter[_value_in_next]:
            ...

        def in_(
            self, __value: _value_in[Union[date, str]]
        ) -> Filter[_value_in[Union[date, str]]]:
            ...

        def not_in(
            self, __value: _value_not_in[Union[date, str]]
        ) -> Filter[_value_not_in[Union[date, str]]]:
            ...

        def in_calendar_day(
            self, __value: _value_in_calendar_day
        ) -> Filter[_value_in_calendar_day]:
            ...

        def in_calendar_week(
            self, __value: _value_in_calendar_week
        ) -> Filter[_value_in_calendar_week]:
            ...

        def in_calendar_month(
            self, __value: _value_in_calendar_month
        ) -> Filter[_value_in_calendar_month]:
            ...

        def __eq__(
            self, __value: _value_is[Union[date, str]]
        ) -> Filter[_value_is[Union[date, str]]]:
            ...

        def __ne__(
            self, __value: _value_is_not[Union[date, str]]
        ) -> Filter[_value_is_not[Union[date, str]]]:
            ...

        def __lt__(
            self, __value: _value_less_than[Union[date, str]]
        ) -> Filter[_value_less_than[Union[date, str]]]:
            ...

        def __gt__(
            self, __value: _value_greater_than[Union[date, str]]
        ) -> Filter[_value_greater_than[Union[date, str]]]:
            ...


DateTimeCastTo = TypeVar("DateTimeCastTo", default=datetime)


class DateTime(ShotgunType, Generic[DateTimeCastTo]):
    _output_type = datetime

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> DateTimeCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...

        def is_(
            self, __value: _value_is[Union[datetime, str]]
        ) -> Filter[_value_is[Union[datetime, str]]]:
            ...

        def is_not(
            self, __value: _value_is_not[Union[datetime, str]]
        ) -> Filter[_value_is_not[Union[datetime, str]]]:
            ...

        def less_than(
            self, __value: _value_less_than[Union[datetime, str]]
        ) -> Filter[_value_less_than[Union[datetime, str]]]:
            ...

        def greater_than(
            self, __value: _value_greater_than[Union[datetime, str]]
        ) -> Filter[_value_greater_than[Union[datetime, str]]]:
            ...

        def between(
            self, __value: _value_between[Union[datetime, str]]
        ) -> Filter[_value_between[Union[datetime, str]]]:
            ...

        def in_last(self, __value: _value_in_last) -> Filter[_value_in_last]:
            ...

        def in_next(self, __value: _value_in_next) -> Filter[_value_in_next]:
            ...

        def in_(
            self, __value: _value_in[Union[datetime, str]]
        ) -> Filter[_value_in[Union[datetime, str]]]:
            ...

        def not_in(
            self, __value: _value_not_in[Union[datetime, str]]
        ) -> Filter[_value_not_in[Union[datetime, str]]]:
            ...

        def in_calendar_day(
            self, __value: _value_in_calendar_day
        ) -> Filter[_value_in_calendar_day]:
            ...

        def in_calendar_week(
            self, __value: _value_in_calendar_week
        ) -> Filter[_value_in_calendar_week]:
            ...

        def in_calendar_month(
            self, __value: _value_in_calendar_month
        ) -> Filter[_value_in_calendar_month]:
            ...

        def __eq__(
            self, __value: _value_is[Union[datetime, str]]
        ) -> Filter[_value_is[Union[datetime, str]]]:
            ...

        def __ne__(
            self, __value: _value_is_not[Union[datetime, str]]
        ) -> Filter[_value_is_not[Union[datetime, str]]]:
            ...

        def __lt__(
            self, __value: _value_less_than[Union[datetime, str]]
        ) -> Filter[_value_less_than[Union[datetime, str]]]:
            ...

        def __gt__(
            self, __value: _value_greater_than[Union[datetime, str]]
        ) -> Filter[_value_greater_than[Union[datetime, str]]]:
            ...


DurationCastTo = TypeVar("DurationCastTo", default=timedelta)


class Duration(ShotgunType, Generic[DurationCastTo]):
    _output_type = timedelta

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> DurationCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...

        def is_(
            self, __value: _value_is[Union[timedelta, int]]
        ) -> Filter[_value_is[Union[timedelta, int]]]:
            ...

        def is_not(
            self, __value: _value_is_not[Union[timedelta, int]]
        ) -> Filter[_value_is_not[Union[timedelta, int]]]:
            ...

        def less_than(
            self, __value: _value_less_than[Union[timedelta, int]]
        ) -> Filter[_value_less_than[Union[timedelta, int]]]:
            ...

        def greater_than(
            self, __value: _value_greater_than[Union[timedelta, int]]
        ) -> Filter[_value_greater_than[Union[timedelta, int]]]:
            ...

        def between(
            self, __value: _value_between[Union[timedelta, int]]
        ) -> Filter[_value_between[Union[timedelta, int]]]:
            ...

        def in_(
            self, __value: _value_in[Union[timedelta, int]]
        ) -> Filter[_value_in[Union[timedelta, int]]]:
            ...

        def not_in(
            self, __value: _value_not_in[Union[timedelta, int]]
        ) -> Filter[_value_not_in[Union[timedelta, int]]]:
            ...

        def __eq__(
            self, __value: _value_is[Union[timedelta, int]]
        ) -> Filter[_value_is[Union[timedelta, int]]]:
            ...

        def __ne__(
            self, __value: _value_is_not[Union[timedelta, int]]
        ) -> Filter[_value_is_not[Union[timedelta, int]]]:
            ...

        def __lt__(
            self, __value: _value_less_than[Union[timedelta, int]]
        ) -> Filter[_value_less_than[Union[timedelta, int]]]:
            ...

        def __gt__(
            self, __value: _value_greater_than[Union[timedelta, int]]
        ) -> Filter[_value_greater_than[Union[timedelta, int]]]:
            ...


EntityCastTo = TypeVar("EntityCastTo", default=GenericEntity)


class Entity(ShotgunType, Generic[EntityCastTo]):
    _output_type = GenericEntity

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> EntityCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...

        def is_(
            self, __value: _value_is[EntityObject]
        ) -> Filter[_value_is[EntityObject]]:
            ...

        def is_not(
            self, __value: _value_is_not[EntityObject]
        ) -> Filter[_value_is_not[EntityObject]]:
            ...

        def in_(
            self, __value: _value_in[EntityObject]
        ) -> Filter[_value_in[EntityObject]]:
            ...

        def not_in(
            self, __value: _value_not_in[EntityObject]
        ) -> Filter[_value_not_in[EntityObject]]:
            ...

        def type_is(
            self, __value: _value_type_is[EntityType]
        ) -> Filter[_value_type_is[EntityType]]:
            ...

        def type_is_not(
            self, __value: _value_type_is_not[EntityType]
        ) -> Filter[_value_type_is_not[EntityType]]:
            ...

        def name_contains(
            self, __value: _value_name_contains
        ) -> Filter[_value_name_contains]:
            ...

        def name_not_contains(
            self, __value: _value_name_not_contains
        ) -> Filter[_value_name_not_contains]:
            ...

        def name_starts_with(
            self, __value: _value_name_starts_with
        ) -> Filter[_value_name_starts_with]:
            ...

        def name_ends_with(
            self, __value: _value_name_ends_with
        ) -> Filter[_value_name_ends_with]:
            ...

        def __eq__(
            self, __value: _value_is[EntityObject]
        ) -> Filter[_value_is[EntityObject]]:
            ...

        def __ne__(
            self, __value: _value_is_not[EntityObject]
        ) -> Filter[_value_is_not[EntityObject]]:
            ...


class Footage(Text, Generic[TextCastTo]):
    pass


class Image(Text, Generic[TextCastTo]):
    pass


ListCastTo = TypeVar("ListCastTo", default=str)


class List(ShotgunType, Generic[ListCastTo]):
    _output_type = str

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> ListCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...

        def is_(self, __value: _value_is[str]) -> Filter[_value_is[str]]:
            ...

        def is_not(self, __value: _value_is_not[str]) -> Filter[_value_is_not[str]]:
            ...

        def in_(self, __value: _value_in[str]) -> Filter[_value_in[str]]:
            ...

        def not_in(self, __value: _value_not_in[str]) -> Filter[_value_not_in[str]]:
            ...

        def __eq__(self, __value: _value_is[str]) -> Filter[_value_is[str]]:
            ...

        def __ne__(self, __value: _value_is_not[str]) -> Filter[_value_is_not[str]]:
            ...


class Password(Text, Generic[TextCastTo]):
    pass


class Percent(Number, Generic[NumberCastTo]):
    pass


SerializableCastTo = TypeVar("SerializableCastTo", default=dict)


class Serializable(ShotgunType, Generic[SerializableCastTo]):
    _output_type = dict

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> SerializableCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...


class StatusList(List, Generic[ListCastTo]):
    pass


SummaryCastTo = TypeVar("SummaryCastTo", default=str)


class Summary(ShotgunType, Generic[SummaryCastTo]):
    _output_type = str


TagListCastTo = TypeVar("TagListCastTo", default=List[str])


class TagList(ShotgunType, Generic[TagListCastTo]):
    _output_type = list

    if typing.TYPE_CHECKING:

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> TagListCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...


class Timecode(Number, Generic[NumberCastTo]):
    pass


class Url(Serializable, Generic[SerializableCastTo]):
    pass


__all__ = [
    "UnknownFieldType",
    "Text",
    "Float",
    "MultiEntity",
    "Number",
    "Addressing",
    "Checkbox",
    "Color",
    "Currency",
    "Date",
    "DateTime",
    "Duration",
    "Entity",
    "Footage",
    "Image",
    "List",
    "Password",
    "Percent",
    "Serializable",
    "StatusList",
    "Summary",
    "TagList",
    "Timecode",
    "Url",
]
