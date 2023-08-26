import pytest
import safegrid

from safegrid.filters import Filter, FilterGroup, FilterGroupOperator, FilterOperator


def test_convert_to_sg_filter():
    filter_a = Filter("code", FilterOperator.Is, "test")
    filter_b = Filter("users", FilterOperator.Contains, "user_name")

    group = FilterGroup(filters=[filter_a, filter_b], operator=FilterGroupOperator.All)

    assert group.to_sg_filter() == {
        "filter_operator": "all",
        "filters": [["code", "is", "test"], ["users", "contains", "user_name"]],
    }


def test_filter_group():
    """You can also join Filter Groups with | and &"""
    filter_a = Filter("code", FilterOperator.Is, "test")
    filter_b = Filter("users", FilterOperator.Contains, "user_name")
    filter_c = Filter("id", FilterOperator.Is, 1)
    filter_d = Filter("id", FilterOperator.LessThan, 2)

    any_group = FilterGroup(
        filters=[filter_a, filter_b], operator=FilterGroupOperator.Any
    )
    all_group = FilterGroup(
        filters=[filter_c, filter_d], operator=FilterGroupOperator.All
    )

    # AND-ing two groups makes a new group
    new_group = all_group & any_group
    assert isinstance(new_group, FilterGroup)
    assert new_group.operator == FilterGroupOperator.All
    assert set(new_group.filters) == {all_group, any_group}

    # OR-ing two groups makes a new group
    new_group = all_group | any_group
    assert isinstance(new_group, FilterGroup)
    assert new_group.operator == FilterGroupOperator.Any
    assert set(new_group.filters) == {all_group, any_group}

    # AND-ing a filter to an all_group makes a copy of the group with the filter added
    new_group = all_group & filter_a
    assert isinstance(new_group, FilterGroup)
    assert set(new_group.filters) == {filter_c, filter_d, filter_a}

    # OR-ing a filter to an all_group makes a new group
    new_group = all_group | filter_a
    assert isinstance(new_group, FilterGroup)
    assert new_group.operator == FilterGroupOperator.Any
    assert set(new_group.filters) == {all_group, filter_a}

    # AND-ing a filter to an any_group makes a new group
    new_group = any_group & filter_c
    assert isinstance(new_group, FilterGroup)
    assert new_group.operator == FilterGroupOperator.All
    assert set(new_group.filters) == {any_group, filter_c}

    # OR-ing a filter to an any_group makes a copy of the group with the filter added
    new_group = any_group | filter_c
    assert isinstance(new_group, FilterGroup)
    assert set(new_group.filters) == {filter_a, filter_b, filter_c}

    # you can also +
    new_group = all_group + any_group
    assert isinstance(new_group, FilterGroup)
    assert set(new_group.filters) == {all_group, any_group}

    # you can't add other things to a group!
    with pytest.raises(TypeError):
        any_group & "not a filter"  # type: ignore
    with pytest.raises(TypeError):
        any_group | "not a filter"  # type: ignore


def test_filter_joins():
    """You can join filters with & and |."""
    filter_a = Filter("code", FilterOperator.Is, "test")
    filter_b = Filter("users", FilterOperator.Contains, "user_name")
    filter_c = Filter("test", FilterOperator.IsNot, "value")

    # you can "and" two filters together
    and_filter = filter_a & filter_b
    assert isinstance(and_filter, FilterGroup)
    assert and_filter.operator == FilterGroupOperator.All
    assert set(and_filter.filters) == {filter_a, filter_b}

    # or +
    and_filter = filter_a + filter_b
    assert isinstance(and_filter, FilterGroup)
    assert and_filter.operator == FilterGroupOperator.All
    assert set(and_filter.filters) == {filter_a, filter_b}

    # or "or" two filters together
    or_filter = filter_a | filter_b
    assert isinstance(or_filter, FilterGroup)
    assert or_filter.operator == FilterGroupOperator.Any
    assert set(or_filter.filters) == {filter_a, filter_b}

    # Adding a group to a filter does the same thing as adding a filter to a group
    group = FilterGroup(filters=[filter_c], operator=FilterGroupOperator.All)

    new_group = filter_a & group
    assert isinstance(new_group, FilterGroup)
    assert new_group.operator == FilterGroupOperator.All
    assert set(new_group.filters) == {filter_a, filter_c}

    new_group = filter_a | group
    assert isinstance(new_group, FilterGroup)
    assert new_group.operator == FilterGroupOperator.Any
    assert set(new_group.filters) == {filter_a, group}

    # you can't add other things to a filter!
    with pytest.raises(TypeError):
        filter_a & "not a filter"  # type: ignore
    with pytest.raises(TypeError):
        filter_a | "not a filter"  # type: ignore


def test_print():
    filter_a = Filter("code", FilterOperator.Is, "test")
    print(filter_a)
    str(filter_a)

    group = FilterGroup(filters=[filter_a], operator=FilterGroupOperator.All)
    print(group)
    str(group)
