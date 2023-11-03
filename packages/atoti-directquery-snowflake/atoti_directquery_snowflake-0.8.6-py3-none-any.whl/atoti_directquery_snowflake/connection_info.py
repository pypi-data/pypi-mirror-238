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

from .connection import SnowflakeConnection
from .table import SnowflakeTable


class SnowflakeConnectionInfo(
    ExternalDatabaseConnectionInfo[SnowflakeConnection, SnowflakeTable]
):
    """Information needed to connect to a Snowflake database."""

    @doc(**_EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS)
    def __init__(
        self,
        url: str,
        /,
        *,
        password: Optional[str] = None,
        feeding_warehouse_name: Optional[str] = None,
        array_agg_wrapper_function_name: Optional[str] = None,
        time_travel: bool = True,
    ):
        """Create a Snowflake connection info.

        Args:
            url: The JDBC connection string.
                See https://docs.snowflake.com/en/user-guide/jdbc-configure.html#jdbc-driver-connection-string for more information.
            {password}
            feeding_warehouse_name: The name of the warehouse to use for the initial feeding.
                If ``None``, the main warehouse will be used.
            array_agg_wrapper_function_name: The name of the User Defined Function to use to wrap the aggregations on arrays to improve performance.
                    This function must be defined in Snowflake and accessible to the role running the queries.
            time_travel: Whether to use time travel in queries.

        Example:
            >>> import os
            >>> from atoti_directquery_snowflake import SnowflakeConnectionInfo
            >>> connection_info = SnowflakeConnectionInfo(
            ...     "jdbc:snowflake://"
            ...     + os.environ["SNOWFLAKE_ACCOUNT_IDENTIFIER"]
            ...     + ".snowflakecomputing.com/?user="
            ...     + os.environ["SNOWFLAKE_USERNAME"],
            ...     password=os.environ["SNOWFLAKE_PASSWORD"],
            ... )

        """
        super().__init__(
            database_key="SNOWFLAKE",
            options={
                "FEEDING_WAREHOUSE_NAME": feeding_warehouse_name,
                "ARRAY_AGG_WRAPPER_FUNCTION_NAME": array_agg_wrapper_function_name,
                "ENABLE_TIME_TRAVEL": "true" if time_travel else "false",
            },
            password=password,
            url=url,
        )

    @override
    def _get_database_connection(self, java_api: JavaApi) -> SnowflakeConnection:
        return SnowflakeConnection(
            database_key=self._database_key,
            java_api=java_api,
        )
