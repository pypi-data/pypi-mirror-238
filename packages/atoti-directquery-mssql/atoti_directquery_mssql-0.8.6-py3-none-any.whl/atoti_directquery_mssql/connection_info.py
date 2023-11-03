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

from .connection import MsSqlConnection
from .table import MsSqlTable


class MsSqlConnectionInfo(ExternalDatabaseConnectionInfo[MsSqlConnection, MsSqlTable]):
    """Information needed to connect to a Microsoft SQL Server database."""

    @doc(**_EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS)
    def __init__(
        self,
        url: str,
        /,
        *,
        password: Optional[str] = None,
    ):
        """Create a Microsoft SQL Server connection info.

        Args:
            url: The JDBC connection string.
                See https://learn.microsoft.com/en-us/sql/connect/jdbc/building-the-connection-url?view=sql-server-ver16 for more information.
            {password}
        """
        super().__init__(database_key="MS_SQL", password=password, url=url)

    @override
    def _get_database_connection(self, java_api: JavaApi) -> MsSqlConnection:
        return MsSqlConnection(
            database_key=self._database_key,
            java_api=java_api,
        )
