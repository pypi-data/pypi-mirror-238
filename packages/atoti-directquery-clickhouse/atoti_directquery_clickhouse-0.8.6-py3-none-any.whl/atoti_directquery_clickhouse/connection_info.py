from typing import Optional

from atoti._docs_utils import (
    EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS as _EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS,
)
from atoti._java_api import JavaApi
from atoti.directquery._external_database_connection_info import (
    ExternalDatabaseConnectionInfo,
)
from atoti_core import doc
from typing_extensions import override

from .connection import ClickhouseConnection
from .table import ClickhouseTable


class ClickhouseConnectionInfo(
    ExternalDatabaseConnectionInfo[ClickhouseConnection, ClickhouseTable]
):
    """Information needed to connect to a ClickHouse database."""

    @doc(**_EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS)
    def __init__(
        self,
        url: str,
        /,
        *,
        password: Optional[str] = None,
    ):
        """Create a ClickHouse connection info.

        Args:
            url: The connection string.
                The pattern is: ``(clickhouse|ch):(https|http|...)://login:password@host:port/database?prop=value``.
                For example: ``"clickhouse:https://user:password@localhost:8123/mydb"``.
                When a parameter is missing, the default value will be used.
            {password}
        """
        super().__init__(database_key="CLICKHOUSE", password=password, url=url)

    @override
    def _get_database_connection(self, java_api: JavaApi) -> ClickhouseConnection:
        return ClickhouseConnection(
            database_key=self._database_key,
            java_api=java_api,
        )
