from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from http import HTTPStatus
from typing import Optional, TypedDict, Union, cast
from urllib.error import HTTPError
from urllib.parse import urlencode

from atoti_core import ActiveViamClient
from typing_extensions import TypeGuard

from ._constants import ROLE_ADMIN, ROLE_ATOTI_ROOT, USER_CONTENT_STORAGE_NAMESPACE


class _ContentEntry(TypedDict):
    # A `TypeDict` cannot be `Generic` (https://github.com/python/mypy/issues/3863).
    # Otherwise, `_ContentEntry` could be parametrized so that the value of this property depends on the type of the `ContentTree`.
    isDirectory: bool
    timestamp: int
    lastEditor: str
    owners: Sequence[str]
    readers: Sequence[str]
    canRead: bool
    canWrite: bool


class _DirectoryContentEntry(_ContentEntry):
    ...


class _FileContentEntry(_ContentEntry):
    content: str


ContentEntry = Union[_DirectoryContentEntry, _FileContentEntry]


class _DirectoryContentTreeOptionalProperties(TypedDict, total=False):
    # Pyright does not support recursive types.
    children: Mapping[str, ContentTree]  # pyright: ignore[reportUndefinedVariable]
    """Missing when there are no children."""


class _DirectoryContentTree(_DirectoryContentTreeOptionalProperties):
    entry: _DirectoryContentEntry


class _FileContentTree(TypedDict):
    entry: _FileContentEntry


ContentTree = Union[_DirectoryContentTree, _FileContentTree]


def is_directory(tree: ContentTree, /) -> TypeGuard[_DirectoryContentTree]:
    return tree["entry"]["isDirectory"]


def is_file(tree: ContentTree, /) -> TypeGuard[_FileContentTree]:
    return not is_directory(tree)


class ContentClient:
    def __init__(self, *, client: ActiveViamClient) -> None:
        self._client = client

    def get(self, path: str, /) -> Optional[ContentTree]:
        try:
            response = self._client.fetch_json(
                namespace=USER_CONTENT_STORAGE_NAMESPACE,
                query=urlencode({"path": path}),
                route="files",
            )
        except HTTPError as error:
            if error.code == HTTPStatus.NOT_FOUND:
                return None
            raise
        else:
            return cast(ContentTree, response.body)

    def create(self, path: str, /, *, content: object) -> None:
        self._client.fetch_json(
            body={
                "content": json.dumps(content),
                "owners": [ROLE_ATOTI_ROOT, ROLE_ADMIN],
                "readers": [ROLE_ATOTI_ROOT, ROLE_ADMIN],
                "overwrite": True,
                "recursive": True,
            },
            method="PUT",
            namespace=USER_CONTENT_STORAGE_NAMESPACE,
            query=urlencode({"path": path}),
            raw=True,
            route="files",
        )

    def delete(self, path: str, /) -> None:
        self._client.fetch_json(
            method="DELETE",
            namespace=USER_CONTENT_STORAGE_NAMESPACE,
            query=urlencode({"path": path}),
            raw=True,
            route="files",
        )
