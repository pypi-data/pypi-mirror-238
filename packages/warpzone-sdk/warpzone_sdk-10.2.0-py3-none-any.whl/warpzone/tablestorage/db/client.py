from functools import cache
from typing import Optional

import pandas as pd
from azure.core.credentials import (
    AzureNamedKeyCredential,
    AzureSasCredential,
    TokenCredential,
)
from azure.identity import DefaultAzureCredential

from warpzone.blobstorage.client import WarpzoneBlobClient
from warpzone.healthchecks import HealthCheckResult, check_health_of
from warpzone.tablestorage.db import base_client
from warpzone.tablestorage.tables.client import WarpzoneTableClient


class WarpzoneDatabaseClient:
    """Class to interact with Azure Table Storage for database queries
    (using Azure Blob Service underneath)
    """

    def __init__(
        self, table_client: WarpzoneTableClient, blob_client: WarpzoneBlobClient
    ):
        self._table_client = table_client
        self._blob_client = blob_client

    @classmethod
    def from_resource_name(
        cls,
        storage_account: str,
        credential: AzureNamedKeyCredential
        | AzureSasCredential
        | TokenCredential = DefaultAzureCredential(),
    ):
        table_client = WarpzoneTableClient.from_resource_name(
            storage_account, credential
        )
        blob_client = WarpzoneBlobClient.from_resource_name(storage_account, credential)

        return cls(
            table_client,
            blob_client,
        )

    @classmethod
    def from_connection_string(cls, conn_str: str):
        table_client = WarpzoneTableClient.from_connection_string(conn_str)
        blob_client = WarpzoneBlobClient.from_connection_string(conn_str)

        return cls(table_client, blob_client)

    @cache
    def _query_to_pandas(self, table_name: str, query: str):
        records = self._table_client.query(table_name, query)
        df = base_client.generate_dataframe_from_records(records, self._blob_client)

        return df

    @cache
    def get_table_metadata(self, table_name: str):
        query = f"PartitionKey eq '{table_name}'"
        records = self._table_client.query(base_client.METADATA_TABLE_NAME, query)

        if len(records) == 0:
            raise ValueError(f"No metadata found for table {table_name}")
        if len(records) > 1:
            raise ValueError(f"Multiple metadata records found for table {table_name}")

        metadata = records[0]
        metadata.pop("PartitionKey")
        metadata.pop("RowKey")

        return metadata

    def query(
        self,
        table_name: str,
        time_interval: Optional[pd.Interval] = None,
        filters: Optional[dict[str, object]] = None,
        use_cache: Optional[bool] = True,
    ):
        # To support tables that does not yet have the metadata table entry.
        # We try to get the metadata, but if it fails, we assume that the table
        # is not a blob table.
        try:
            table_metadata = self.get_table_metadata(table_name)
            is_blob_table = table_metadata["store_to_blob"]
        except ValueError:
            is_blob_table = False

        if is_blob_table:
            query = base_client.generate_query_string(time_interval)
        else:
            query = base_client.generate_query_string(time_interval, filters)

        if use_cache:
            df = self._query_to_pandas(table_name, query)
        else:
            # Use __wrapped__ to bypass cache
            df = self._query_to_pandas.__wrapped__(self, table_name, query)

        if is_blob_table and filters:
            df = base_client.filter_dataframe(df, filters)

        return df

    def check_health(self) -> HealthCheckResult:
        """
        Pings the connections to the client's associated storage
        ressources in Azure.
        """

        health_check = check_health_of(self._table_client)

        return health_check
