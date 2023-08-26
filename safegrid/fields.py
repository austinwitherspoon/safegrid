from datetime import date, datetime, timedelta
from typing_extensions import Self, TypeVar, TypedDict
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from typing_extensions import (
    Any,
    Generic,
    Optional,
    Protocol,
    Type,
    Union,
    overload,
)
import typing

from .filters import (
    Filter,
    FilterOperator,
    _value_is,
    _value_is_not,
    _value_less_than,
    _value_greater_than,
    _value_contains,
    _value_not_contains,
    _value_starts_with,
    _value_ends_with,
    _value_between,
    _value_in_last,
    _value_in_next,
    _value_in,
    _value_not_in,
    _value_type_is,
    _value_type_is_not,
    _value_in_calendar_day,
    _value_in_calendar_week,
    _value_in_calendar_month,
    _value_name_contains,
    _value_name_not_contains,
    _value_name_starts_with,
    _value_name_ends_with,
)
from ._types import GenericEntity


class ShotgunType:
    _output_type = None
    _pydantic_schema = None

    def __init__(self, name: str, pydantic_field: FieldInfo):
        self._name = name
        self.field_info = pydantic_field

    @property
    def name(self) -> str:
        return self.field_info.alias or self._name

    if typing.TYPE_CHECKING:  # pragma: no cover

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
    if typing.TYPE_CHECKING:  # pragma: no cover

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


class TextField(ShotgunType, Generic[TextCastTo]):
    _output_type = str

    if typing.TYPE_CHECKING:  # pragma: no cover

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


class FloatField(ShotgunType, Generic[FloatCastTo]):
    _output_type = float

    if typing.TYPE_CHECKING:  # pragma: no cover

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


class MultiEntityField(ShotgunType, Generic[EntityCastTo]):
    _output_type = typing.List[GenericEntity]

    if typing.TYPE_CHECKING:  # pragma: no cover  # pragma: no cover

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


class NumberField(ShotgunType, Generic[NumberCastTo]):
    _output_type = int

    if typing.TYPE_CHECKING:  # pragma: no cover

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


class AddressingField(MultiEntityField, Generic[EntityCastTo]):
    pass


CheckboxCastTo = TypeVar("CheckboxCastTo", default=bool)


class CheckboxField(ShotgunType, Generic[CheckboxCastTo]):
    _output_type = bool

    if typing.TYPE_CHECKING:  # pragma: no cover

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


class ColorField(TextField, Generic[TextCastTo]):
    """Color field type in shotgrid.
    value:	str
    example:	255,0,0 | pipeline_step

    pipeline_step indicates the Task color inherits from the Pipeline Step color.
    """


class CurrencyField(FloatField, Generic[FloatCastTo]):
    pass


DateCastTo = TypeVar("DateCastTo", default=date)


class DateField(ShotgunType, Generic[DateCastTo]):
    _output_type = date

    if typing.TYPE_CHECKING:  # pragma: no cover

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


class DateTimeField(ShotgunType, Generic[DateTimeCastTo]):
    _output_type = datetime

    if typing.TYPE_CHECKING:  # pragma: no cover

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


class DurationField(ShotgunType, Generic[DurationCastTo]):
    _output_type = timedelta

    if typing.TYPE_CHECKING:  # pragma: no cover

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


class EntityField(ShotgunType, Generic[EntityCastTo]):
    _output_type = GenericEntity

    if typing.TYPE_CHECKING:  # pragma: no cover

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


class FootageField(TextField, Generic[TextCastTo]):
    pass


class ImageField(TextField, Generic[TextCastTo]):
    pass


ListCastTo = TypeVar("ListCastTo", default=str)


class ListField(ShotgunType, Generic[ListCastTo]):
    _output_type = str

    if typing.TYPE_CHECKING:  # pragma: no cover

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


class PasswordField(TextField, Generic[TextCastTo]):
    pass


class PercentField(NumberField, Generic[NumberCastTo]):
    pass


SerializableCastTo = TypeVar("SerializableCastTo", default=dict)


class SerializableField(ShotgunType, Generic[SerializableCastTo]):
    _output_type = dict

    if typing.TYPE_CHECKING:  # pragma: no cover

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> SerializableCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...


class StatusListField(ListField, Generic[ListCastTo]):
    pass


SummaryCastTo = TypeVar("SummaryCastTo", default=str)


class SummaryField(ShotgunType, Generic[SummaryCastTo]):
    _output_type = str


TagListCastTo = TypeVar("TagListCastTo", default=ListField[str])


class TagListField(ShotgunType, Generic[TagListCastTo]):
    _output_type = list

    if typing.TYPE_CHECKING:  # pragma: no cover

        @overload
        def __get__(self, instance: None, owner: Any) -> Self:
            ...

        @overload
        def __get__(self, instance: object, owner: Any) -> TagListCastTo:
            ...

        def __get__(self, instance: Optional[object], owner: Any) -> Any:
            ...


class TimecodeField(NumberField, Generic[NumberCastTo]):
    pass


class UrlField(SerializableField, Generic[SerializableCastTo]):
    pass


__all__ = [
    "UnknownFieldType",
    "TextField",
    "FloatField",
    "MultiEntityField",
    "NumberField",
    "AddressingField",
    "CheckboxField",
    "ColorField",
    "CurrencyField",
    "DateField",
    "DateTimeField",
    "DurationField",
    "EntityField",
    "FootageField",
    "ImageField",
    "ListField",
    "PasswordField",
    "PercentField",
    "SerializableField",
    "StatusListField",
    "SummaryField",
    "TagListField",
    "TimecodeField",
    "UrlField",
]
