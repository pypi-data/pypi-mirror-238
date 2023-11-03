from collections.abc import Mapping

import atoti as tt
from atoti._external_table_identifier import ExternalTableIdentifier
from atoti.directquery._external_database_with_cache_connection import (
    ExternalDatabaseWithCacheConnection,
)
from typing_extensions import override

from .table import SnowflakeTable


class SnowflakeConnection(ExternalDatabaseWithCacheConnection[SnowflakeTable]):
    """Connection to an external Snowflake database.

    Use :meth:`atoti.Session.connect_to_external_database` to create one.

    Example :

    .. doctest::
        :hide:

        >>> import os
        >>> from atoti_directquery_snowflake import SnowflakeConnectionInfo
        >>> connection_info = SnowflakeConnectionInfo(
        ...     f"jdbc:snowflake://{os.environ['SNOWFLAKE_ACCOUNT_IDENTIFIER']}.snowflakecomputing.com/?user={os.environ['SNOWFLAKE_USERNAME']}&database=TEST_RESOURCES&schema=TESTS",
        ...     password=os.environ["SNOWFLAKE_PASSWORD"],
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
    ) -> SnowflakeTable:
        return SnowflakeTable(identifier, database_key=self._database_key, types=types)
