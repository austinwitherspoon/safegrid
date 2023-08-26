import typing
from enum import Enum

from typing_extensions import (
    TYPE_CHECKING,
    Any,
    Generic,
    Iterable,
    Literal,
    Optional,
    Tuple,
    TypeAlias,
    TypeVar,
    Union,
    overload,
)


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
        ) -> "Filter[_value_is]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.IsNot],
            value: _value_is_not,
        ) -> "Filter[_value_is_not]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.LessThan],
            value: _value_less_than,
        ) -> "Filter[_value_less_than]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.GreaterThan],
            value: _value_greater_than,
        ) -> "Filter[_value_greater_than]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.Contains],
            value: _value_contains,
        ) -> "Filter[_value_contains]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NotContains],
            value: _value_not_contains,
        ) -> "Filter[_value_not_contains]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.StartsWith],
            value: _value_starts_with,
        ) -> "Filter[_value_starts_with]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.EndsWith],
            value: _value_ends_with,
        ) -> "Filter[_value_ends_with]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.Between],
            value: _value_between,
        ) -> "Filter[_value_between]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.InLast],
            value: _value_in_last,
        ) -> "Filter[_value_in_last]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.InNext],
            value: _value_in_next,
        ) -> "Filter[_value_in_next]":
            ...

        @overload
        def __new__(
            cls, field: str, operator: Literal[FilterOperator.In], value: _value_in
        ) -> "Filter[_value_in]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NotIn],
            value: _value_not_in,
        ) -> "Filter[_value_not_in]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.TypeIs],
            value: _value_type_is,
        ) -> "Filter[_value_type_is]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.TypeIsNot],
            value: _value_type_is_not,
        ) -> "Filter[_value_type_is_not]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.InCalendarDay],
            value: _value_in_calendar_day,
        ) -> "Filter[_value_in_calendar_day]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.InCalendarWeek],
            value: _value_in_calendar_week,
        ) -> "Filter[_value_in_calendar_week]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.InCalendarMonth],
            value: _value_in_calendar_month,
        ) -> "Filter[_value_in_calendar_month]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NameContains],
            value: _value_name_contains,
        ) -> "Filter[_value_name_contains]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NameNotContains],
            value: _value_name_not_contains,
        ) -> "Filter[_value_name_not_contains]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NameStartsWith],
            value: _value_name_starts_with,
        ) -> "Filter[_value_name_starts_with]":
            ...

        @overload
        def __new__(
            cls,
            field: str,
            operator: Literal[FilterOperator.NameEndsWith],
            value: _value_name_ends_with,
        ) -> "Filter[_value_name_ends_with]":
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
