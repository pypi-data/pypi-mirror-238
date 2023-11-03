from collections.abc import Mapping

import atoti as tt
from atoti._external_table_identifier import ExternalTableIdentifier
from atoti.directquery._external_database_connection import (
    ExternalDatabaseConnection,
)
from typing_extensions import override

from .table import DatabricksTable


class DatabricksConnection(ExternalDatabaseConnection[DatabricksTable]):
    """Connection to an external Databricks database.

    Use :meth:`atoti.Session.connect_to_external_database` to create one.

    Example :

    .. doctest::
        :hide:

        >>> import os
        >>> from atoti_directquery_databricks import DatabricksConnectionInfo
        >>> connection_info = DatabricksConnectionInfo(
        ...     f"jdbc:databricks://{os.environ['DATABRICKS_SERVER_HOSTNAME']}/default;"
        ...     + "transportMode=http;"
        ...     + "ssl=1;"
        ...     + f"httpPath={os.environ['DATABRICKS_HTTP_PATH']};"
        ...     + "AuthMech=3;"
        ...     + "UID=token;",
        ...     password=os.environ["DATABRICKS_AUTH_TOKEN"],
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
    ) -> DatabricksTable:
        return DatabricksTable(identifier, database_key=self._database_key, types=types)
