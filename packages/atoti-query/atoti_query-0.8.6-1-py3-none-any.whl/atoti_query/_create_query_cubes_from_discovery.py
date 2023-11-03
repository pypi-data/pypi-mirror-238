from __future__ import annotations

from typing import Optional

from atoti_core import (
    HierarchyIdentifier,
    ImmutableMapping,
    LevelIdentifier,
    MeasureIdentifier,
)

from ._discovery import (
    IndexedDiscovery,
    IndexedDiscoveryCube,
    IndexedDiscoveryHierarchy,
)
from ._execute_gaq import ExecuteGaq
from ._query_mdx import QueryMdx
from .query_cube import QueryCube
from .query_cubes import QueryCubes
from .query_hierarchies import QueryHierarchies
from .query_hierarchy import QueryHierarchy
from .query_level import QueryLevel
from .query_measure import QueryMeasure
from .query_measures import QueryMeasures


def _create_hierarchy(
    hierarchy: IndexedDiscoveryHierarchy,
    /,
    *,
    dimension_name: str,
) -> QueryHierarchy:
    hierarchy_identifier = HierarchyIdentifier(dimension_name, hierarchy["name"])
    levels = ImmutableMapping(
        {
            level["name"]: QueryLevel(
                LevelIdentifier(hierarchy_identifier, level["name"])
            )
            for level in hierarchy["levels"].values()
            if level["type"] != "ALL"
        }
    )
    return QueryHierarchy(
        hierarchy_identifier,
        levels=levels,
        slicing=hierarchy["slicing"],
    )


def _create_cube(
    cube: IndexedDiscoveryCube,
    /,
    *,
    execute_gaq: Optional[ExecuteGaq] = None,
    query_mdx: QueryMdx,
) -> QueryCube:
    hierarchies = QueryHierarchies(
        {
            (dimension["name"], hierarchy["name"]): _create_hierarchy(
                hierarchy, dimension_name=dimension["name"]
            )
            for dimension in cube["dimensions"].values()
            if dimension["name"] != "Epoch"
            for hierarchy in dimension["hierarchies"].values()
        }
    )
    measures = QueryMeasures(
        {
            measure["name"]: QueryMeasure(
                MeasureIdentifier(measure["name"]),
                description=measure.get("description"),
                folder=measure.get("folder"),
                formatter=measure.get("formatString"),
                visible=measure["visible"],
            )
            for measure in cube["measures"].values()
        }
    )
    return QueryCube(
        cube["name"],
        cube=cube,
        execute_gaq=execute_gaq,
        hierarchies=hierarchies,
        measures=measures,
        query_mdx=query_mdx,
    )


def create_query_cubes_from_discovery(
    discovery: IndexedDiscovery,
    /,
    *,
    execute_gaq: Optional[ExecuteGaq] = None,
    query_mdx: QueryMdx,
) -> QueryCubes:
    return QueryCubes(
        {
            cube["name"]: _create_cube(
                cube, execute_gaq=execute_gaq, query_mdx=query_mdx
            )
            for catalog in discovery["catalogs"].values()
            for cube in catalog["cubes"].values()
        }
    )
