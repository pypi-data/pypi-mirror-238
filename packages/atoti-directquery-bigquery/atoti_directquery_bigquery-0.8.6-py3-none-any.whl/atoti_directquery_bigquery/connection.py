from collections.abc import Mapping

import atoti as tt
from atoti._external_table_identifier import ExternalTableIdentifier
from atoti.directquery._external_database_with_cache_connection import (
    ExternalDatabaseWithCacheConnection,
)
from typing_extensions import override

from .table import BigqueryTable


class BigqueryConnection(ExternalDatabaseWithCacheConnection[BigqueryTable]):
    """Connection to an external BigQuery database.

    Use :meth:`atoti.Session.connect_to_external_database` to create one.

    Example:
        >>> from atoti_directquery_bigquery import BigqueryConnectionInfo
        >>> connection_info = BigqueryConnectionInfo()
        >>> external_database = session.connect_to_external_database(connection_info)
    """

    @override
    def _create_table(
        self,
        identifier: ExternalTableIdentifier,
        /,
        *,
        types: Mapping[str, tt.DataType],
    ) -> BigqueryTable:
        return BigqueryTable(identifier, database_key=self._database_key, types=types)
