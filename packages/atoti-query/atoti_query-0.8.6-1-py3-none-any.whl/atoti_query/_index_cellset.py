from __future__ import annotations

from ._cellset import CellSet, CellSetAxis, IndexedCellSet, NormalizedCellSetAxis


def _get_max_level_per_hierarchy(axis: CellSetAxis, /) -> list[int]:
    return [
        max(
            (
                len(position[hierarchy_index]["namePath"])
                for position in axis["positions"]
            ),
            default=0,
        )
        for hierarchy_index in range(len(axis["hierarchies"]))
    ]


def _normalize_cellset_axis(axis: CellSetAxis, /) -> NormalizedCellSetAxis:
    return {
        "hierarchies": axis["hierarchies"],
        "id": axis["id"],
        "maxLevelPerHierarchy": _get_max_level_per_hierarchy(axis),
        "positions": axis["positions"],
    }


def index_cellset(cellset: CellSet, /) -> IndexedCellSet:
    """Index the CellSet cells by ordinal to provide faster access.

    This also adds the ``maxLevelPerHierarchy`` property to the axes.
    """
    return {
        "axes": [_normalize_cellset_axis(axis) for axis in cellset["axes"]],
        "cells": {cell["ordinal"]: cell for cell in cellset["cells"]},
        "cube": cellset["cube"],
        "defaultMembers": cellset["defaultMembers"],
    }
