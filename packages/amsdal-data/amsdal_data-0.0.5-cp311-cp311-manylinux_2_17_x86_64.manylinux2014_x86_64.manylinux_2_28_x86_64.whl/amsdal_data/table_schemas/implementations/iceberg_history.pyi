from amsdal_data.connections.implementations.iceberg_history import IcebergHistoricalConnection as IcebergHistoricalConnection
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.data_models.iceberg_table_column import IcebergTableColumnsSchema as IcebergTableColumnsSchema
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.models.data_models.table_schema import TableSchema as TableSchema

class IcebergHistoryTableSchemaService(TableSchemaServiceBase):
    connection: IcebergHistoricalConnection
    def register_table(self, table_schema: TableSchema) -> tuple[str, bool]: ...
    def create_table(self, table_name: str, table_schema: TableSchema) -> None: ...
    def unregister_table(self, address: Address) -> None: ...
