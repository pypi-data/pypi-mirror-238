from collections.abc import Iterable, Mapping
from dataclasses import dataclass, replace
from datetime import timedelta
from functools import cached_property
from math import ceil
from pathlib import Path
from typing import Any, Literal, Optional, Union, cast

import pandas as pd
import pyarrow as pa
from atoti_core import (
    DEFAULT_QUERY_TIMEOUT as _DEFAULT_QUERY_TIMEOUT,
    EMPTY_MAPPING as _EMPTY_MAPPING,
    PLUGINS as _PLUGINS,
    ActiveViamClient,
    BaseSession,
    BaseSessionBound,
    Constant,
    Context,
    HierarchyIsinCondition,
    LevelIdentifier,
    MeasureIdentifier,
    Plugin,
    QueryFilter,
    decombine_condition,
    doc,
    keyword_only_dataclass,
)
from typing_extensions import override

from ._arrow_to_pandas import arrow_to_pandas
from ._cellset import CellSet
from ._cellset_to_query_result import cellset_to_query_result
from ._create_query_cubes_from_discovery import create_query_cubes_from_discovery
from ._discovery import Discovery, IndexedDiscovery
from ._get_data_types import GetDataTypes
from ._index_cellset import index_cellset
from ._index_discovery import index_discovery
from ._widget_conversion_details import WidgetConversionDetails
from .auth import Auth
from .client_certificate import ClientCertificate
from .query_cubes import QueryCubes
from .security import Security

_VERSIONS_WITHOUT_RAW_MODE = ("4", "5")


def _serialize_condition(condition: QueryFilter) -> dict[str, Any]:
    (
        level_conditions,
        level_isin_conditions,
        hierarchy_isin_conditions,
    ) = decombine_condition(
        condition,
        allowed_subject_types=(LevelIdentifier,),
        allowed_comparison_operators=("eq",),
        allowed_target_types=(Constant,),
        allowed_combination_operators=("and",),
        allowed_isin_element_types=(Constant,),
    )[
        0
    ]

    if hierarchy_isin_conditions:
        raise ValueError(
            f"""Unsupported `{HierarchyIsinCondition.__name__}` in `mode="raw"` query."""
        )

    # Ensure all condition are == or isin on strings
    for level_condition in level_conditions:
        if not isinstance(level_condition.target.value, str):
            raise TypeError(
                f"Type {type(level_condition.target.value)} not supported in query condition: level conditions can only be based on equality with strings."
            )
    for level_isin_condition in level_isin_conditions:
        not_string = [
            value.value
            for value in level_isin_condition.elements
            if not isinstance(value.value, str)
        ]
        if not_string:
            raise TypeError(
                f"Only strings are supported in query condition but the following values are not strings: {not_string}."
            )

    # Serialize the conditions
    equal_conditions = {
        level_condition.subject.java_description: level_condition.target.value
        for level_condition in level_conditions
    }
    isin_conditions = {
        level_condition.subject.java_description: [
            member.value for member in level_condition.elements
        ]
        for level_condition in level_isin_conditions
    }
    return {
        "equalConditions": equal_conditions,
        "isinConditions": isin_conditions,
        "neConditions": {},
    }


def _enrich_context(
    context: Context,
    *,
    timeout: timedelta,
) -> Context:
    return {
        "queriesTimeLimit": ceil(timeout.total_seconds()),
        **context,
    }


@keyword_only_dataclass
@dataclass(frozen=True)
class _QuerySessionPrivateParameters:
    client: Optional[ActiveViamClient] = None
    plugins: Optional[Mapping[str, Plugin]] = None


@keyword_only_dataclass
@dataclass(frozen=True)
class _QueryMdxPrivateParameters:
    get_data_types: Optional[GetDataTypes] = None
    session: Optional[BaseSessionBound] = None


class QuerySession(BaseSession[QueryCubes, Security]):
    """Used to query a remote Atoti session.

    Note:
        The cube and table structure of a query session is expected to be immutable.
    """

    @doc(url="{url}")
    def __init__(
        self,
        url: str,
        *,
        auth: Optional[Auth] = None,
        certificate_authority: Optional[Union[str, Path]] = None,
        client_certificate: Optional[ClientCertificate] = None,
        **kwargs: Any,
    ):
        """Create a query session.

        Args:
            url: The base URL of the session.
                The endpoint ``f"{url}/versions/rest"`` is expected to exist.
            auth: The authentication to use to access the session.
            certificate_authority: Path to the custom certificate authority file to use to verify the HTTPS connection.
                Required when the session has been configured with a certificate that is not signed by some trusted public certificate authority.
            client_certificate: The client certificate to authenticate against the session.
        """
        super().__init__()

        private_parameters = _QuerySessionPrivateParameters(**kwargs)

        assert not private_parameters.client or private_parameters.client.url == url

        self._auth = auth
        self.__client = private_parameters.client or ActiveViamClient(
            url,
            auth=auth,
            certificate_authority=Path(certificate_authority)
            if certificate_authority
            else None,
            client_certificate=Path(client_certificate.certificate)
            if client_certificate
            else None,
            client_certificate_keyfile=Path(client_certificate.keyfile)
            if client_certificate and client_certificate.keyfile
            else None,
            client_certificate_password=client_certificate.password
            if client_certificate
            else None,
        )

        plugins = (
            _PLUGINS.default
            if private_parameters.plugins is None
            else private_parameters.plugins
        )

        for plugin in plugins.values():
            plugin.post_init_session(self)

    @property
    @override
    def cubes(self) -> QueryCubes:
        """Cubes of the session."""
        return self._cubes

    @cached_property
    def _cubes(self) -> QueryCubes:
        return create_query_cubes_from_discovery(
            self._discovery,
            execute_gaq=self._execute_gaq if self._gaq_supported else None,
            query_mdx=self.query_mdx,
        )

    @property
    @override
    def _security(self) -> Security:
        return self.__security

    @cached_property
    def __security(self) -> Security:
        return Security(client=self._client)

    @property
    def url(self) -> str:
        """URL of the session."""
        return self._client.url

    @property
    @override
    def _client(self) -> ActiveViamClient:
        return self.__client

    @property
    @override
    def _location(self) -> Mapping[str, object]:
        return {"url": self.url}

    @property
    @override
    def _local_url(self) -> str:
        return self.url

    def _execute_arrow_query(
        self,
        body: object,
        /,
        *,
        namespace: str,
        route: str,
    ) -> pd.DataFrame:
        with self._client.fetch_json(
            body=body,
            namespace=namespace,
            raw=True,
            route=route,
        ) as response:
            record_batch_stream = pa.ipc.open_stream(response)
            schema = record_batch_stream.schema
            for name in schema.names:
                schema.field(name).with_nullable(True)  # noqa: FBT003
            table = pa.Table.from_batches(record_batch_stream, schema=schema)

        return arrow_to_pandas(table)

    @property
    def _raw_query_mode_supported(self) -> bool:
        return any(
            version["id"] not in _VERSIONS_WITHOUT_RAW_MODE
            for version in self._client.server_versions["apis"][self._pivot_namespace][
                "versions"
            ]
        )

    @property
    def _gaq_supported(self) -> bool:
        return self._client.has_atoti_python_api_endpoints

    def _execute_gaq(
        self,
        *,
        cube_name: str,
        filter: Optional[QueryFilter] = None,  # noqa: A002
        include_empty_rows: bool,
        include_totals: bool,
        level_identifiers: Iterable[LevelIdentifier],
        measure_identifiers: Iterable[MeasureIdentifier],
        scenario: str,
        timeout: timedelta,
    ) -> pd.DataFrame:
        if include_empty_rows:
            raise NotImplementedError(
                "Empty rows cannot be included with this query mode."
            )

        if include_totals:
            raise NotImplementedError("Totals cannot be included with this query mode.")

        body = {
            "cubeName": cube_name,
            "branch": scenario,
            "measures": [
                measure_identifier.measure_name
                for measure_identifier in measure_identifiers
            ],
            "levelCoordinates": [
                level_identifier.java_description
                for level_identifier in level_identifiers
            ],
            **(
                {"equalConditions": {}, "isinConditions": {}, "neConditions": {}}
                if filter is None
                else _serialize_condition(filter)
            ),
            "timeout": ceil(timeout.total_seconds()),
        }
        return self._execute_arrow_query(body, namespace="atoti", route="arrow/query")

    @override
    def _generate_auth_headers(self) -> dict[str, str]:
        return dict(self._auth(self.url)) if self._auth else {}

    @property
    def _pivot_namespace(self) -> str:
        return next(
            namespace
            for namespace in [
                "activeviam/pivot",
                "pivot",  # Atoti Server < 6.0.0-M1.
            ]
            if namespace in self._client.server_versions["apis"]
        )

    def _fetch_discovery(self) -> Discovery:
        """Return the discovery for this session.

        Note:
            For faster access to discovery elements, use the :attr:`_discovery` property.
        """
        response = self._client.fetch_json(
            namespace=self._pivot_namespace, route="cube/discovery"
        )
        return cast(Discovery, response.body)

    @cached_property
    def _discovery(self) -> IndexedDiscovery:
        return index_discovery(self._fetch_discovery())

    def _query_mdx_to_cellset(
        self, mdx: str, *, context: Context = _EMPTY_MAPPING
    ) -> CellSet:
        response = self._client.fetch_json(
            body={
                "context": {**context},
                "mdx": mdx,
            },
            namespace=self._pivot_namespace,
            route="cube/query/mdx",
        )
        return cast(CellSet, response.body)

    @override
    def query_mdx(
        self,
        mdx: str,
        *,
        keep_totals: bool = False,
        timeout: timedelta = _DEFAULT_QUERY_TIMEOUT,
        mode: Literal["pretty", "raw"] = "pretty",
        context: Context = _EMPTY_MAPPING,
        **kwargs: Any,
    ) -> pd.DataFrame:
        private_parameters = _QueryMdxPrivateParameters(**kwargs)

        context = _enrich_context(context, timeout=timeout)

        if mode == "raw":
            if not self._raw_query_mode_supported:
                raise ValueError(
                    "`raw` mode not supported by this Atoti Server version."
                )

            return self._execute_arrow_query(
                {
                    "jsonMdxQuery": {"mdx": mdx, "context": context},
                    "outputConfiguration": {"format": "arrow"},
                },
                namespace=self._pivot_namespace,
                route="cube/dataexport/download",
            )

        cellset = self._query_mdx_to_cellset(mdx, context=context)
        indexed_cellset = index_cellset(cellset)
        query_result = cellset_to_query_result(
            indexed_cellset,
            context=context,
            discovery=self._discovery,
            get_data_types=private_parameters.get_data_types,
            keep_totals=keep_totals,
        )
        # Let local sessions pass their reference to have the correct name and widget creation code.
        session = private_parameters.session or self

        widget_creation_code = session._get_widget_creation_code()
        if widget_creation_code is not None and query_result._atoti_metadata:
            query_result._atoti_metadata = replace(
                query_result._atoti_metadata,
                widget_conversion_details=WidgetConversionDetails(
                    mdx=mdx,
                    sessionId=session._id,
                    widgetCreationCode=widget_creation_code,
                ),
            )

        return query_result
