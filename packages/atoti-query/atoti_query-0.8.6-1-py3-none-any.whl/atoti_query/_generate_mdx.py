from collections.abc import Collection, Iterable, Mapping, Sequence
from typing import Literal, Optional

from atoti_core import (
    BASE_SCENARIO_NAME,
    ComparisonCondition,
    Constant,
    HierarchyIdentifier,
    HierarchyIsinCondition,
    IsinCondition,
    LevelIdentifier,
    MeasureIdentifier,
    QueryFilter,
    decombine_condition,
)

from ._discovery import IndexedDiscoveryCube, IndexedDiscoveryHierarchy
from ._hierarchy_filter import HierarchyFilter


def _escape(name: str, /) -> str:
    return name.replace("]", "]]")


def _generate_set(
    members: Collection[str], /, *, single_element_short_syntax: bool = True
) -> str:
    if single_element_short_syntax and len(members) == 1:
        return next(iter(members))

    return f"""{{{", ".join(members)}}}"""


def _generate_columns_set(measure_identifiers: Iterable[MeasureIdentifier], /) -> str:
    return _generate_set(
        [
            f"[Measures].[{_escape(measure_identifier.measure_name)}]"
            for measure_identifier in measure_identifiers
        ],
        # Atoti UI 5 does not support it.
        # See https://support.activeviam.com/jira/browse/UI-5036.
        single_element_short_syntax=False,
    )


def _keep_only_deepest_levels(
    level_identifiers: Iterable[LevelIdentifier],
    /,
    *,
    cube: IndexedDiscoveryCube,
) -> dict[LevelIdentifier, int]:
    hierarchy_to_max_level_depth: dict[HierarchyIdentifier, int] = {}

    for level_identifier in level_identifiers:
        hierarchy_identifier = level_identifier.hierarchy_identifier
        current_max_level_depth = hierarchy_to_max_level_depth.get(
            hierarchy_identifier, -1
        )
        regular_level_names = [
            level["name"]
            for level in cube["dimensions"][hierarchy_identifier.dimension_name][
                "hierarchies"
            ][hierarchy_identifier.hierarchy_name]["levels"].values()
        ]
        level_depth = regular_level_names.index(level_identifier.level_name)

        if level_depth > current_max_level_depth:
            hierarchy_to_max_level_depth[hierarchy_identifier] = level_depth

    return {
        LevelIdentifier(
            hierarchy_identifier,
            list(
                cube["dimensions"][hierarchy_identifier.dimension_name]["hierarchies"][
                    hierarchy_identifier.hierarchy_name
                ]["levels"]
            )[depth],
        ): depth
        for hierarchy_identifier, depth in hierarchy_to_max_level_depth.items()
    }


def _get_first_level(hierarchy: IndexedDiscoveryHierarchy, /) -> str:
    return next(iter(hierarchy["levels"])) if hierarchy["slicing"] else "ALL"


def _generate_hierarchy_unique_name(
    hierarchy_identifier: HierarchyIdentifier,
    /,
    *,
    cube: IndexedDiscoveryCube,
    include_first_level: bool = False,
) -> str:
    parts = [hierarchy_identifier.dimension_name, hierarchy_identifier.hierarchy_name]

    if include_first_level:
        hierarchy = cube["dimensions"][hierarchy_identifier.dimension_name][
            "hierarchies"
        ][hierarchy_identifier.hierarchy_name]
        parts.append(_get_first_level(hierarchy))

    return ".".join(f"[{_escape(part)}]" for part in parts)


def _generate_level_set(
    level_identifier: LevelIdentifier,
    /,
    *,
    cube: IndexedDiscoveryCube,
    include_totals: bool,
    level_depth: int,
) -> str:
    hierarchy = cube["dimensions"][
        level_identifier.hierarchy_identifier.dimension_name
    ]["hierarchies"][level_identifier.hierarchy_identifier.hierarchy_name]
    return (
        f"{_generate_hierarchy_unique_name(level_identifier.hierarchy_identifier, cube=cube)}.[{_escape(level_identifier.level_name)}].Members"
        if hierarchy["slicing"] or not include_totals
        else f"Hierarchize(Descendants({{{_generate_hierarchy_unique_name(level_identifier.hierarchy_identifier, cube=cube, include_first_level=True)}.[AllMember]}}, {level_depth}, SELF_AND_BEFORE))"
    )


def _generate_rows_set(
    level_identifiers: Mapping[LevelIdentifier, int],
    /,
    *,
    cube: IndexedDiscoveryCube,
    include_totals: bool,
) -> str:
    if len(level_identifiers) == 1:
        level_identifier, level_depth = next(iter(level_identifiers.items()))
        return _generate_level_set(
            level_identifier,
            cube=cube,
            include_totals=include_totals,
            level_depth=level_depth,
        )

    return f"""Crossjoin({", ".join(
        [
            _generate_level_set(level_identifier, cube=cube,include_totals=include_totals, level_depth=level_depth)
            for level_identifier, level_depth in level_identifiers.items()
        ]
    )})"""


def _ensure_condition_on_shallowest_level(
    level_identifier: LevelIdentifier,
    /,
    *,
    cube: IndexedDiscoveryCube,
) -> None:
    if (
        next(
            level["name"]
            for level in cube["dimensions"][
                level_identifier.hierarchy_identifier.dimension_name
            ]["hierarchies"][level_identifier.hierarchy_identifier.hierarchy_name][
                "levels"
            ].values()
            if level["type"] != "ALL"
        )
        != level_identifier.level_name
    ):
        raise (
            ValueError(
                f"Only conditions based on the shallowest level of a hierarchy are supported but level {level_identifier!r} was given."
            )
        )


def _generate_hierarchy_identifier_to_filter(
    *,
    comparison_conditions: Iterable[
        ComparisonCondition[LevelIdentifier, Literal["eq", "ne"], Constant]
    ],
    cube: IndexedDiscoveryCube,
    hierarchy_isin_conditions: Iterable[HierarchyIsinCondition],
    isin_conditions: Iterable[IsinCondition[LevelIdentifier, Constant]],
) -> dict[HierarchyIdentifier, HierarchyFilter]:
    hierarchy_identifier_to_filter: dict[HierarchyIdentifier, HierarchyFilter] = {}

    def add_hierarchy_filter(
        hierarchy_filter: HierarchyFilter,
        /,
        *,
        hierarchy_identifier: HierarchyIdentifier,
    ) -> None:
        existing_filter = hierarchy_identifier_to_filter.get(hierarchy_identifier)

        hierarchy_identifier_to_filter[hierarchy_identifier] = (
            existing_filter & hierarchy_filter if existing_filter else hierarchy_filter
        )

    for comparison_condition in comparison_conditions:
        _ensure_condition_on_shallowest_level(comparison_condition.subject, cube=cube)

        add_hierarchy_filter(
            HierarchyFilter(
                exclusion=comparison_condition.operator == "ne",
                member_paths=[(comparison_condition.target,)],
            ),
            hierarchy_identifier=comparison_condition.subject.hierarchy_identifier,
        )

    for isin_condition in isin_conditions:
        _ensure_condition_on_shallowest_level(isin_condition.subject, cube=cube)

        add_hierarchy_filter(
            HierarchyFilter(
                member_paths=[(member,) for member in isin_condition.elements],
            ),
            hierarchy_identifier=isin_condition.subject.hierarchy_identifier,
        )

    for hierarchy_isin_condition in hierarchy_isin_conditions:
        add_hierarchy_filter(
            HierarchyFilter(
                member_paths=hierarchy_isin_condition.member_paths,
            ),
            hierarchy_identifier=hierarchy_isin_condition.subject,
        )

    return hierarchy_identifier_to_filter


def _generate_member_unique_name(
    member_path: Iterable[Constant],
    /,
    *,
    cube: IndexedDiscoveryCube,
    hierarchy_identifier: HierarchyIdentifier,
) -> str:
    hierarchy = cube["dimensions"][hierarchy_identifier.dimension_name]["hierarchies"][
        hierarchy_identifier.hierarchy_name
    ]
    parts = [
        _generate_hierarchy_unique_name(
            hierarchy_identifier, cube=cube, include_first_level=True
        ),
        *([] if hierarchy["slicing"] else ["[AllMember]"]),
        *(f"[{_escape(str(member.json))}]" for member in member_path),
    ]

    return ".".join(parts)


def _generate_filter(
    hierarchy_filter: HierarchyFilter,
    /,
    *,
    cube: IndexedDiscoveryCube,
    hierarchy_identifier: HierarchyIdentifier,
) -> str:
    filter_set = _generate_set(
        [
            _generate_member_unique_name(
                member_path, cube=cube, hierarchy_identifier=hierarchy_identifier
            )
            for member_path in hierarchy_filter.member_paths
        ]
    )

    return (
        f"Except({_generate_hierarchy_unique_name(hierarchy_identifier, cube=cube)}.Members,{filter_set})"
        if hierarchy_filter.exclusion
        else filter_set
    )


def _generate_filters(
    hierarchy_identifier_to_filter: Mapping[HierarchyIdentifier, HierarchyFilter],
    /,
    *,
    cube: IndexedDiscoveryCube,
    scenario_name: str,
) -> list[str]:
    filters = [
        _generate_filter(
            hierarchy_filter,
            cube=cube,
            hierarchy_identifier=hierarchy_identifier,
        )
        for hierarchy_identifier, hierarchy_filter in hierarchy_identifier_to_filter.items()
    ]

    if scenario_name != BASE_SCENARIO_NAME:
        filters.append(
            _generate_member_unique_name(
                [Constant(scenario_name)],
                cube=cube,
                hierarchy_identifier=HierarchyIdentifier("Epoch", "Epoch"),
            )
        )

    return filters


def _generate_from_clause(
    filters: Sequence[str],
    /,
    *,
    cube: IndexedDiscoveryCube,
) -> str:
    from_cube = f"""FROM [{_escape(cube["name"])}]"""

    if not filters:
        return from_cube

    return f"FROM (SELECT {filters[-1]} ON COLUMNS {_generate_from_clause(filters[0:-1], cube=cube)})"


def _generate_mdx_with_decombined_conditions(
    *,
    comparison_conditions: Iterable[
        ComparisonCondition[LevelIdentifier, Literal["eq", "ne"], Constant]
    ] = (),
    cube: IndexedDiscoveryCube,
    hierarchy_isin_conditions: Iterable[HierarchyIsinCondition] = (),
    include_empty_rows: bool = False,
    include_totals: bool = False,
    isin_conditions: Iterable[IsinCondition[LevelIdentifier, Constant]] = (),
    level_identifiers: Iterable[LevelIdentifier],
    measure_identifiers: Iterable[MeasureIdentifier],
    scenario_name: str,
) -> str:
    mdx = f"SELECT {_generate_columns_set(measure_identifiers)} ON COLUMNS"

    deepest_levels = _keep_only_deepest_levels(level_identifiers, cube=cube)

    if deepest_levels:
        mdx = f"{mdx}, {'' if include_empty_rows else 'NON EMPTY '}{_generate_rows_set(deepest_levels, cube=cube, include_totals=include_totals)} ON ROWS"

    hierarchy_identifier_to_filter = _generate_hierarchy_identifier_to_filter(
        comparison_conditions=comparison_conditions,
        cube=cube,
        hierarchy_isin_conditions=hierarchy_isin_conditions,
        isin_conditions=isin_conditions,
    )

    filters = _generate_filters(
        hierarchy_identifier_to_filter,
        cube=cube,
        scenario_name=scenario_name,
    )

    return f"{mdx} {_generate_from_clause(filters, cube=cube)}"


def generate_mdx(
    *,
    cube: IndexedDiscoveryCube,
    filter: Optional[QueryFilter] = None,  # noqa: A002
    include_empty_rows: bool = False,
    include_totals: bool = False,
    level_identifiers: Iterable[LevelIdentifier] = (),
    measure_identifiers: Iterable[MeasureIdentifier] = (),
    scenario: str = BASE_SCENARIO_NAME,
) -> str:
    """Return the corresponding MDX query.

    The value of the measures is given on all the members of the given levels.
    If no level is specified then the value at the top level is returned.
    """
    allowed_comparison_operators: tuple[Literal["eq", "ne"], ...] = ("eq", "ne")

    comparison_conditions, isin_conditions, hierarchy_isin_conditions = (
        ((), (), ())
        if filter is None
        else decombine_condition(
            filter,
            allowed_subject_types=(LevelIdentifier,),
            allowed_comparison_operators=allowed_comparison_operators,
            allowed_target_types=(Constant,),
            allowed_combination_operators=("and",),
            allowed_isin_element_types=(Constant,),
        )[0]
    )

    return _generate_mdx_with_decombined_conditions(
        comparison_conditions=comparison_conditions,
        cube=cube,
        hierarchy_isin_conditions=hierarchy_isin_conditions,
        include_empty_rows=include_empty_rows,
        include_totals=include_totals,
        isin_conditions=isin_conditions,
        level_identifiers=level_identifiers,
        measure_identifiers=measure_identifiers,
        scenario_name=scenario,
    )
