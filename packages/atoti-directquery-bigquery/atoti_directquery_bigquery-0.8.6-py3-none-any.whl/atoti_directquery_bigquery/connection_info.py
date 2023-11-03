from typing import Optional

from atoti._java_api import JavaApi
from atoti.directquery._external_database_connection_info import (
    ExternalDatabaseConnectionInfo,
)
from atoti_core import PathLike, local_to_absolute_path
from typing_extensions import override

from .connection import BigqueryConnection
from .table import BigqueryTable


class BigqueryConnectionInfo(
    ExternalDatabaseConnectionInfo[BigqueryConnection, BigqueryTable]
):
    """Information needed to connect to a BigQuery database."""

    def __init__(
        self,
        credentials: Optional[PathLike] = None,
        /,
        *,
        time_travel: bool = True,
    ):
        """Create a BigQuery connection info.

        Args:
            credentials: The path to the `BigQuery credentials file <https://cloud.google.com/docs/authentication/getting-started#setting_the_environment_variable>`__.
                If ``None``, the `application default credentials <https://cloud.google.com/java/docs/reference/google-auth-library/latest/com.google.auth.oauth2.GoogleCredentials#com_google_auth_oauth2_GoogleCredentials_getApplicationDefault__>`__ will be used.
            time_travel: Whether to use time travel in queries.

        Example:
            >>> from atoti_directquery_bigquery import BigqueryConnectionInfo
            >>> connection_info = BigqueryConnectionInfo()

        """
        super().__init__(
            database_key="BIGQUERY",
            url=None if credentials is None else local_to_absolute_path(credentials),
            options={
                "ENABLE_TIME_TRAVEL": "true" if time_travel else "false",
            },
        )

    @override
    def _get_database_connection(self, java_api: JavaApi) -> BigqueryConnection:
        return BigqueryConnection(
            database_key=self._database_key,
            java_api=java_api,
        )
