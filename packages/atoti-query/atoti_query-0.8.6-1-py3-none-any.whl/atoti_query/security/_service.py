from __future__ import annotations

import json
from collections.abc import Iterable, Set as AbstractSet
from pathlib import Path

from ._authentication_type import AuthenticationType
from ._content_client import ContentClient, ContentTree, is_directory, is_file
from ._restriction import Restriction
from ._restriction_from_mapping import restriction_from_mapping
from ._restriction_to_dict import restriction_to_dict

_ROOT_DIRECTORY = "/atoti/security"
_COLUMN_RESTRICTIONS_DIRECTORY = f"{_ROOT_DIRECTORY}/column_restrictions"
_COLUMN_RESTRICTIONS_PATH_TEMPLATE = (
    f"{_COLUMN_RESTRICTIONS_DIRECTORY}/{{role_name}}.json"
)
_DEFAULT_ROLES_FILE_PATH_TEMPLATE = (
    f"{_ROOT_DIRECTORY}/default_roles/{{authentication_type}}.json"
)
_INDIVIDUAL_ROLES_DIRECTORY = f"{_ROOT_DIRECTORY}/individual_roles"
_INDIVIDUAL_ROLES_FILE_PATH_TEMPLATE = (
    f"{_INDIVIDUAL_ROLES_DIRECTORY}/{{username}}.json"
)
_ROLE_MAPPING_FILE_PATH_TEMPLATE = (
    f"{_ROOT_DIRECTORY}/role_mapping/{{authentication_type}}.json"
)


def _get_role_mapping_file_path(authentication_type: AuthenticationType, /) -> str:
    return _ROLE_MAPPING_FILE_PATH_TEMPLATE.format(
        authentication_type=authentication_type,
    )


def _get_default_roles_file_path(authentication_type: AuthenticationType, /) -> str:
    return _DEFAULT_ROLES_FILE_PATH_TEMPLATE.format(
        authentication_type=authentication_type
    )


def _get_individual_roles_file_path_for_user(username: str, /) -> str:
    return _INDIVIDUAL_ROLES_FILE_PATH_TEMPLATE.format(username=username)


def _restriction_from_mapping(tree: ContentTree, /) -> Restriction:
    assert is_file(tree)
    restriction: dict[str, dict[str, list[str]]] = json.loads(
        tree["entry"]["content"],
    )
    return restriction_from_mapping(restriction)


class Service:
    """Handle the REST communication to configure the session security."""

    def __init__(self, *, client: ContentClient) -> None:
        super().__init__()

        self._client = client

    @property
    def restrictions(self) -> dict[str, Restriction]:
        tree = self._client.get(_COLUMN_RESTRICTIONS_DIRECTORY)

        if not tree:
            return {}

        assert is_directory(tree)

        return {
            Path(filename).stem: _restriction_from_mapping(tree)
            for filename, tree in tree.get("children", {}).items()
        }

    def upsert_restriction(
        self, restriction: Restriction, /, *, role_name: str
    ) -> None:
        path = _COLUMN_RESTRICTIONS_PATH_TEMPLATE.format(role_name=role_name)

        self._client.create(
            path,
            content=restriction_to_dict(restriction),
        )

    def delete_restriction(self, role_name: str, /) -> None:
        path = _COLUMN_RESTRICTIONS_PATH_TEMPLATE.format(role_name=role_name)
        self._client.delete(path)

    def get_role_mapping(
        self, *, authentication_type: AuthenticationType
    ) -> dict[str, list[str]]:
        tree = self._client.get(_get_role_mapping_file_path(authentication_type))

        if not tree:
            return {}

        assert is_file(tree)

        mapping: dict[str, list[str]] = json.loads(tree["entry"]["content"])
        return mapping

    def upsert_role_mapping(
        self,
        role_name: str,
        /,
        *,
        authentication_type: AuthenticationType,
        authorities: Iterable[str],
    ) -> None:
        role_mapping = self.get_role_mapping(authentication_type=authentication_type)
        role_mapping[role_name] = list(authorities)
        self._client.create(
            _get_role_mapping_file_path(authentication_type),
            content=role_mapping,
        )

    def remove_role_from_role_mapping(
        self,
        role_name: str,
        /,
        *,
        authentication_type: AuthenticationType,
    ) -> None:
        role_mapping = self.get_role_mapping(authentication_type=authentication_type)
        del role_mapping[role_name]
        self._client.create(
            _get_role_mapping_file_path(authentication_type),
            content=role_mapping,
        )

    @property
    def individual_roles(self) -> dict[str, list[str]]:
        tree = self._client.get(_INDIVIDUAL_ROLES_DIRECTORY)

        if not tree:
            return {}

        assert is_directory(tree)

        individual_roles: dict[str, list[str]] = {}

        for path, user_tree in tree.get("children", {}).items():
            assert is_file(user_tree)
            username = Path(path).stem
            individual_roles[username] = json.loads(user_tree["entry"]["content"])

        return individual_roles

    def get_individual_roles_for_user(self, username: str, /) -> list[str]:
        tree = self._client.get(_get_individual_roles_file_path_for_user(username))

        if not tree:
            return []

        assert is_file(tree)

        roles: list[str] = json.loads(tree["entry"]["content"])
        return roles

    def delete_individual_roles_for_user(self, username: str, /) -> None:
        self._client.delete(_get_individual_roles_file_path_for_user(username))

    def upsert_individual_roles(
        self, username: str, /, *, roles: Iterable[str]
    ) -> None:
        final_roles = list(set(roles))
        self._client.create(
            _get_individual_roles_file_path_for_user(username),
            content=final_roles,
        )

    def get_default_roles(self, *, authentication_type: AuthenticationType) -> set[str]:
        tree = self._client.get(_get_default_roles_file_path(authentication_type))

        if not tree:
            return set()

        assert is_file(tree)

        return set(json.loads(tree["entry"]["content"]))

    def set_default_roles(
        self, new_set: AbstractSet[str], /, *, authentication_type: AuthenticationType
    ) -> None:
        self._client.create(
            _get_default_roles_file_path(authentication_type),
            content=list(new_set),
        )

    def clear(self) -> None:
        self._client.delete(_ROOT_DIRECTORY)
