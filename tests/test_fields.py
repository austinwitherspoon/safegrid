from typing import List, Optional, Type

import pydantic.fields
import safegrid
import pytest
from safegrid.fields import (
    ShotgunType,
    UnknownFieldType,
    TextField,
    FloatField,
    MultiEntityField,
    NumberField,
    AddressingField,
    CheckboxField,
    ColorField,
    CurrencyField,
    DateField,
    DateTimeField,
    DurationField,
    EntityField,
    FootageField,
    ImageField,
    ListField,
    PasswordField,
    PercentField,
    SerializableField,
    StatusListField,
    SummaryField,
    TagListField,
    TimecodeField,
    UrlField,
)


FIELD_TYPES: List[Type[ShotgunType]] = [
    UnknownFieldType,
    TextField,
    FloatField,
    MultiEntityField,
    NumberField,
    AddressingField,
    CheckboxField,
    ColorField,
    CurrencyField,
    DateField,
    DateTimeField,
    DurationField,
    EntityField,
    FootageField,
    ImageField,
    ListField,
    PasswordField,
    PercentField,
    SerializableField,
    StatusListField,
    SummaryField,
    TagListField,
    TimecodeField,
    UrlField,
]


def test_filter_generation():
    field_info = pydantic.fields.Field()
    sg_field = ShotgunType("test_field", field_info)

    # Generate an "is" filter from a field
    is_filter = sg_field.is_("value")
    assert isinstance(is_filter, safegrid.filters.Filter)
    # You can also do SQLAlchemy style == filters
    assert is_filter.to_sg_filter() == (sg_field == "value").to_sg_filter()

    # .. and the rest of the filter types
    _filter = sg_field.is_not("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "is_not"
    assert _filter.to_sg_filter() == (sg_field != "value").to_sg_filter()

    _filter = sg_field.less_than("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "less_than"
    assert _filter.to_sg_filter() == (sg_field < "value").to_sg_filter()

    _filter = sg_field.greater_than("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "greater_than"
    assert _filter.to_sg_filter() == (sg_field > "value").to_sg_filter()

    _filter = sg_field.contains("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "contains"

    _filter = sg_field.not_contains("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "not_contains"

    _filter = sg_field.starts_with("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "starts_with"

    _filter = sg_field.ends_with("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "ends_with"

    _filter = sg_field.between("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "between"

    _filter = sg_field.in_("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "in"

    _filter = sg_field.not_in("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "not_in"

    _filter = sg_field.in_last("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "in_last"

    _filter = sg_field.in_next("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "in_next"

    _filter = sg_field.type_is("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "type_is"

    _filter = sg_field.type_is_not("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "type_is_not"

    _filter = sg_field.in_calendar_day("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "in_calendar_day"

    _filter = sg_field.in_calendar_week("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "in_calendar_week"

    _filter = sg_field.in_calendar_month("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "in_calendar_month"

    _filter = sg_field.name_contains("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "name_contains"

    _filter = sg_field.name_not_contains("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "name_not_contains"

    _filter = sg_field.name_starts_with("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "name_starts_with"

    _filter = sg_field.name_ends_with("value")
    assert isinstance(_filter, safegrid.filters.Filter)
    assert _filter.to_sg_filter()[1] == "name_ends_with"

    # shotgrid DOESN'T have >= operators, so make sure we raise an exception
    with pytest.raises(NotImplementedError):
        sg_field >= "value"
    with pytest.raises(NotImplementedError):
        sg_field <= "value"
