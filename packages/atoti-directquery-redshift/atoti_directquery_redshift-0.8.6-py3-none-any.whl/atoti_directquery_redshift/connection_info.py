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

from .connection import RedshiftConnection
from .table import RedshiftTable


class RedshiftConnectionInfo(
    ExternalDatabaseConnectionInfo[RedshiftConnection, RedshiftTable]
):
    """Information needed to connect to a Redshift database."""

    @doc(**_EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS)
    def __init__(
        self,
        url: str,
        /,
        *,
        password: Optional[str] = None,
    ):
        """Create a Redshift connection info.

        Args:
            url: The JDBC connection string.
            {password}

        Example:
                >>> import os
                >>> from atoti_directquery_redshift import RedshiftConnectionInfo
                >>> connection_info = RedshiftConnectionInfo(
                ...     "jdbc:redshift://"
                ...     + os.environ["REDSHIFT_ACCOUNT_IDENTIFIER"]
                ...     + ".redshift.amazonaws.com:5439/dev?user="
                ...     + os.environ["REDSHIFT_USERNAME"]
                ...     + "&schema=test_resources",
                ...     password=os.environ["REDSHIFT_PASSWORD"],
                ... )

        """
        super().__init__(database_key="REDSHIFT", password=password, url=url)

    @override
    def _get_database_connection(self, java_api: JavaApi) -> RedshiftConnection:
        return RedshiftConnection(
            database_key=self._database_key,
            java_api=java_api,
        )
