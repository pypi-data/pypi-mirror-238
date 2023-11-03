from collections.abc import Mapping

import atoti as tt
from atoti._external_table_identifier import ExternalTableIdentifier
from atoti.directquery._external_database_with_cache_connection import (
    ExternalDatabaseWithCacheConnection,
)
from typing_extensions import override

from .table import RedshiftTable


class RedshiftConnection(ExternalDatabaseWithCacheConnection[RedshiftTable]):
    """Connection to an external Redshift database.

    Use :meth:`atoti.Session.connect_to_external_database` to create one.

    Example :

    .. doctest::
        :hide:

        >>> import os
        >>> from atoti_directquery_redshift import RedshiftConnectionInfo
        >>> connection_info = RedshiftConnectionInfo(
        ...     f"jdbc:redshift://{os.environ['REDSHIFT_ACCOUNT_IDENTIFIER']}.redshift.amazonaws.com:5439/dev?user={os.environ['REDSHIFT_USERNAME']}&schema=test_resources",
        ...     password=os.environ["REDSHIFT_PASSWORD"],
        ... )

    .. doctest::

        >>> external_database = session.connect_to_external_database(connection_info)
    """

    @override
    def _create_table(
        self,
        identifier: ExternalTableIdentifier,
        /,
        *,
        types: Mapping[str, tt.DataType],
    ) -> RedshiftTable:
        return RedshiftTable(identifier, database_key=self._database_key, types=types)
