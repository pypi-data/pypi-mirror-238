from collections.abc import Sequence
from typing import Optional, Union

import atoti as tt
from atoti._docs_utils import (
    STANDARD_EXTERNAL_TABLE_OPTIONS_KWARGS as _STANDARD_EXTERNAL_TABLE_OPTIONS_KWARGS,
)
from atoti.directquery._clustering_columns_parameter import (
    CLUSTERING_COLUMNS_PARAMETER as _CLUSTERING_COLUMNS_PARAMETER,
)
from atoti.directquery._external_table_options import ExternalTableOptions
from atoti_core import doc

from .table import DatabricksTable


class DatabricksTableOptions(ExternalTableOptions[DatabricksTable]):
    @doc(**_STANDARD_EXTERNAL_TABLE_OPTIONS_KWARGS)
    def __init__(
        self,
        *,
        array_conversion: Optional[
            Union[tt.MultiColumnArrayConversion, tt.MultiRowArrayConversion]
        ] = None,
        clustering_columns: Sequence[str] = (),
        keys: Optional[Sequence[str]] = None,
    ) -> None:
        """Additional options about the external table to create.

        Args:
            {array_conversion}
            {clustering_columns}
            {keys}

        Example:
            .. doctest:: databricks_table_options
                :hide:

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
                >>> external_database = session.connect_to_external_database(
                ...     connection_info
                ... )

            .. doctest:: databricks_table_options

                >>> from atoti_directquery_databricks import (
                ...     DatabricksTableOptions,
                ... )
                >>> external_table = external_database.tables["tutorial", "sales"]
                >>> table = session.add_external_table(
                ...     external_table,
                ...     table_name="sales_renamed",
                ...     options=DatabricksTableOptions(keys=["SALE_ID"]),
                ... )

            To get arrays from values stored on multiple rows:

            .. doctest:: databricks_table_options

                >>> multi_row_external_table = external_database.tables[
                ...     "tutorial", "multi_row_quantity"
                ... ]
                >>> multi_row_external_table.columns
                ['PRODUCT', 'INDEX', 'QUANTITY']
                >>> multi_row_table = session.add_external_table(
                ...     multi_row_external_table,
                ...     table_name="Sales (Multi row array)",
                ...     options=DatabricksTableOptions(
                ...         array_conversion=tt.MultiRowArrayConversion(
                ...             index_column="INDEX",
                ...             array_columns=["QUANTITY"],
                ...         ),
                ...     ),
                ... )
                >>> multi_row_table.head()
                                                 QUANTITY
                PRODUCT
                product_1  [10.0, 20.0, 15.0, 25.0, 10.0]
                product_2  [50.0, 65.0, 55.0, 30.0, 80.0]

            To get arrays from values stored on multiple columns:

            .. doctest:: databricks_table_options

                >>> multi_column_external_table = external_database.tables[
                ...     "tutorial", "multi_column_quantity"
                ... ]
                >>> multi_column_external_table.columns
                ['PRODUCT', 'QUANTITY_0', 'QUANTITY_1', 'QUANTITY_2', 'QUANTITY_3', 'QUANTITY_4']
                >>> multi_column_table = session.add_external_table(
                ...     multi_column_external_table,
                ...     table_name="Sales (Multi column array)",
                ...     options=DatabricksTableOptions(
                ...         keys=["PRODUCT"],
                ...         array_conversion=tt.MultiColumnArrayConversion(
                ...             column_prefixes=["QUANTITY"],
                ...         ),
                ...     ),
                ... )
                >>> multi_column_table.head()
                                                 QUANTITY
                PRODUCT
                product_1  [10.0, 20.0, 15.0, 25.0, 10.0]
                product_2  [50.0, 65.0, 55.0, 30.0, 80.0]

        """
        super().__init__(
            array_conversion=array_conversion,
            keys=keys,
            options={
                _CLUSTERING_COLUMNS_PARAMETER: clustering_columns
                if clustering_columns
                else None
            },
        )
