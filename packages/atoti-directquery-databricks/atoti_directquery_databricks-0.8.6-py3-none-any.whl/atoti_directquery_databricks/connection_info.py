from typing import Literal, Optional

from atoti._docs_utils import (
    EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS as _EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS,
)
from atoti._java_api import JavaApi
from atoti.directquery._external_database_connection_info import (
    ExternalDatabaseConnectionInfo,
)
from atoti_core import doc
from typing_extensions import override

from .connection import DatabricksConnection
from .table import DatabricksTable


class DatabricksConnectionInfo(
    ExternalDatabaseConnectionInfo[DatabricksConnection, DatabricksTable]
):
    """Information needed to connect to a Databricks database."""

    @doc(**_EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS)
    def __init__(
        self,
        url: str,
        /,
        *,
        password: Optional[str] = None,
        time_travel: Literal[False, "lax", "strict"] = "strict",
    ):
        """Create a Databricks connection info.

        `To aggregate native Databrick arrays, UDAFs (User Defined Aggregation Functions) provided by ActiveViam must be registered on the cluster <https://docs.activeviam.com/products/atoti/server/6.0-next/docs/directquery/databases/databricks/#vectors-support>`__.
        Native array aggregation is not supported on SQL warehouses.

        Args:
            url: The JDBC connection string.
            {password}
            time_travel: How to use Databricks' time travel feature.

                Databricks does not support time travel with views, so the options are:
                - ``False``: tables and views are queried on the latest state of the database.
                - ``"lax"``: tables are queried with time travel but views are queried without it.
                - ``"strict"``: tables are queried with time travel and querying a view raises an error.

        Example:
                >>> import os
                >>> from atoti_directquery_databricks import DatabricksConnectionInfo
                >>> connection_info = DatabricksConnectionInfo(
                ...     "jdbc:databricks://"
                ...     + os.environ["DATABRICKS_SERVER_HOSTNAME"]
                ...     + "/default;"
                ...     + "transportMode=http;"
                ...     + "ssl=1;"
                ...     + "httpPath="
                ...     + os.environ["DATABRICKS_HTTP_PATH"]
                ...     + ";"
                ...     + "AuthMech=3;"
                ...     + "UID=token;",
                ...     password=os.environ["DATABRICKS_AUTH_TOKEN"],
                ... )

        """
        if not time_travel:
            java_time_travel_policy = "DISABLED"
        elif time_travel == "lax":
            java_time_travel_policy = "LAX"
        else:
            java_time_travel_policy = "STRICT"

        super().__init__(
            database_key="DATABRICKS",
            options={
                "TIME_TRAVEL": java_time_travel_policy,
            },
            password=password,
            url=url,
        )

    @override
    def _get_database_connection(self, java_api: JavaApi) -> DatabricksConnection:
        return DatabricksConnection(
            database_key=self._database_key,
            java_api=java_api,
        )
