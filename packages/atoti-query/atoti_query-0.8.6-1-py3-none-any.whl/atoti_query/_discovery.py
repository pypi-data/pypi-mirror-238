from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Optional, TypedDict

from ._named import Named


class DiscoveryLevel(Named):
    caption: str
    type: str  # noqa: A003


class _DiscoveryHierarchy(Named):
    caption: str
    slicing: bool


class DiscoveryHierarchy(_DiscoveryHierarchy):
    levels: Sequence[DiscoveryLevel]


class IndexedDiscoveryHierarchy(_DiscoveryHierarchy):
    levels: Mapping[str, DiscoveryLevel]


class _DiscoveryDimension(Named):
    caption: str
    type: str  # noqa: A003


class DiscoveryDimension(_DiscoveryDimension):
    hierarchies: Sequence[DiscoveryHierarchy]


class IndexedDiscoveryDimension(_DiscoveryDimension):
    hierarchies: Mapping[str, IndexedDiscoveryHierarchy]


class DiscoveryMeasure(Named, TypedDict):
    caption: str
    description: Optional[str]
    folder: Optional[str]
    formatString: Optional[str]
    visible: bool


class DefaultMember(TypedDict):
    captionPath: Sequence[str]
    dimension: str
    hierarchy: str
    path: Sequence[str]


class _DiscoveryCube(Named, TypedDict):
    defaultMembers: Sequence[DefaultMember]


class DiscoveryCube(_DiscoveryCube):
    dimensions: Sequence[DiscoveryDimension]
    measures: Sequence[DiscoveryMeasure]


class IndexedDiscoveryCube(_DiscoveryCube):
    dimensions: Mapping[str, IndexedDiscoveryDimension]
    measures: Mapping[str, DiscoveryMeasure]


class _DiscoveryCatalog(Named):
    ...


class DiscoveryCatalog(_DiscoveryCatalog):
    cubes: Sequence[DiscoveryCube]


class IndexedDiscoveryCatalog(_DiscoveryCatalog):
    cubes: Mapping[str, IndexedDiscoveryCube]


class Discovery(TypedDict):
    catalogs: Sequence[DiscoveryCatalog]


class IndexedDiscovery(TypedDict):
    catalogs: Mapping[str, IndexedDiscoveryCatalog]
