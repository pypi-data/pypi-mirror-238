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

from .connection import SynapseConnection
from .table import SynapseTable


class SynapseConnectionInfo(
    ExternalDatabaseConnectionInfo[SynapseConnection, SynapseTable]
):
    """Information needed to connect to a Synapse database."""

    @doc(**_EXTERNAL_DATABASE_CONNECTION_INFO_KWARGS)
    def __init__(
        self,
        url: str,
        /,
        *,
        password: Optional[str] = None,
    ):
        """Create a Synapse connection info.

        Args:
            url: The JDBC connection string.
                See https://docs.microsoft.com/en-us/azure/synapse-analytics/sql/connection-strings#sample-jdbc-connection-string for more information.
            {password}

        Example:
            .. doctest::
                :hide:

                >>> account_identifier = "tck-directquery-ondemand"

            .. doctest::

                >>> import os
                >>> from atoti_directquery_synapse import SynapseConnectionInfo
                >>> connection_info = SynapseConnectionInfo(
                ...     "jdbc:sqlserver://"
                ...     + account_identifier
                ...     + ".sql.azuresynapse.net;authentication="
                ...     + os.environ["SYNAPSE_AUTHENTICATION_METHOD"]
                ...     + ";user="
                ...     + os.environ["SYNAPSE_USERNAME"],
                ...     password=os.environ["SYNAPSE_PASSWORD"],
                ... )
        """
        super().__init__(database_key="SYNAPSE", password=password, url=url)

    @override
    def _get_database_connection(self, java_api: JavaApi) -> SynapseConnection:
        return SynapseConnection(
            database_key=self._database_key,
            java_api=java_api,
        )
