from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Optional, TypeVar, Union, overload

from ._discovery import (
    Discovery,
    DiscoveryCatalog,
    DiscoveryCube,
    DiscoveryDimension,
    DiscoveryHierarchy,
    IndexedDiscovery,
    IndexedDiscoveryCatalog,
    IndexedDiscoveryCube,
    IndexedDiscoveryDimension,
    IndexedDiscoveryHierarchy,
)
from ._named import Named

_IndexableT_co = TypeVar("_IndexableT_co", bound=Named, covariant=True)
_TransformedT = TypeVar("_TransformedT")


@overload
def _index(iterable: Iterable[_IndexableT_co], /) -> Mapping[str, _IndexableT_co]:
    ...


@overload
def _index(
    iterable: Iterable[_IndexableT_co],
    /,
    *,
    transform: Callable[[_IndexableT_co], _TransformedT],
) -> Mapping[str, _TransformedT]:
    ...


def _index(
    iterable: Iterable[_IndexableT_co],
    /,
    *,
    transform: Optional[Callable[[_IndexableT_co], _TransformedT]] = None,
) -> Mapping[str, Union[_IndexableT_co, _TransformedT]]:
    return {
        element["name"]: transform(element) if transform else element
        for element in iterable
    }


def _index_hierarchy(hierarchy: DiscoveryHierarchy, /) -> IndexedDiscoveryHierarchy:
    return {
        "caption": hierarchy["caption"],
        "levels": _index(hierarchy["levels"]),
        "name": hierarchy["name"],
        "slicing": hierarchy["slicing"],
    }


def _index_dimension(dimension: DiscoveryDimension, /) -> IndexedDiscoveryDimension:
    return {
        "caption": dimension["caption"],
        "hierarchies": _index(dimension["hierarchies"], transform=_index_hierarchy),
        "name": dimension["name"],
        "type": dimension["type"],
    }


def _index_cube(cube: DiscoveryCube, /) -> IndexedDiscoveryCube:
    return {
        "defaultMembers": cube["defaultMembers"],
        "dimensions": _index(cube["dimensions"], transform=_index_dimension),
        "measures": _index(cube["measures"]),
        "name": cube["name"],
    }


def _index_catalog(catalog: DiscoveryCatalog, /) -> IndexedDiscoveryCatalog:
    return {
        "cubes": _index(catalog["cubes"], transform=_index_cube),
        "name": catalog["name"],
    }


def index_discovery(discovery: Discovery, /) -> IndexedDiscovery:
    """Index the discovery by name to provide faster access to its elements."""
    return {
        "catalogs": _index(discovery["catalogs"], transform=_index_catalog),
    }
