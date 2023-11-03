from _typeshed import Incomplete
from amsdal_data.connections.errors import AmsdalConnectionError as AmsdalConnectionError
from amsdal_data.connections.historical_base import HistoricalConnectionBase as HistoricalConnectionBase
from amsdal_data.table_schemas.base import TableSchemaServiceBase as TableSchemaServiceBase
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY, SECONDARY_PARTITION_KEY as SECONDARY_PARTITION_KEY
from amsdal_data.table_schemas.data_models.iceberg_table_column import ComplexType as ComplexType, IcebergDataTypes as IcebergDataTypes, IcebergTableColumn as IcebergTableColumn, ListType as ListType, MapType as MapType, StructType as StructType
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.table_schema import TableColumnSchema
from amsdal_utils.query.data_models.filter import Filter as Filter
from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from amsdal_utils.query.data_models.paginator import CursorPaginator, NumberPaginator
from amsdal_utils.query.data_models.query_specifier import QuerySpecifier as QuerySpecifier
from amsdal_utils.query.enums import Lookup
from amsdal_utils.query.utils import Q
from collections.abc import Callable as Callable
from pydantic import BaseModel
from pyspark.sql import DataFrame as DataFrame, SparkSession
from typing import Any, ClassVar

SUPPORTED_NESTED_FIELDS: Incomplete
logger: Incomplete
resources_dir: Incomplete
DEFAULT_CONNECTION_CONFIGS: Incomplete

def random_string(length: int = ...) -> str: ...

class IcebergTableColumnSchema(TableColumnSchema):
    type: type | ComplexType

address_struct: Incomplete
reference_struct: Incomplete

class SqlOperatorTemplate(BaseModel):
    build_statement: ClassVar[Callable[[Any, str, str, Any], str]]
    build_value: ClassVar[Callable[[Any, Any], Any]]
    template: str | Callable[[Any], str]
    value_template: str | None
    value_modifier: Callable[[Any], Any] | None
    def build_statement(self, field_name: str, filter_key: str, value: Any) -> str: ...
    def build_value(self, value: Any) -> Any: ...

sql_operator_map: dict[Lookup, SqlOperatorTemplate]

class IcebergHistoricalConnection(HistoricalConnectionBase):
    def __init__(self, database_name: str = ..., namespace: str = ...) -> None: ...
    @property
    def table_schema_manager(self) -> TableSchemaServiceBase: ...
    @property
    def connection(self) -> SparkSession: ...
    def connect(self, app_name: str = ..., master_node: str = ..., log_level: str = ..., configs: dict[str, str] | None = ..., **kwargs: Any) -> None:
        """
        Connects to the PySpark cluster. Raises an AmsdalConnectionError if the connection is already established.
        :param app_name: the name of the application
        :type app_name: str
        :param configs: the connection configs parameters to pass to the SparkSession
        :type configs: dict[str, str] | None
        :param kwargs: the connection parameters
        :type kwargs: Any

        :return: None
        """
    def disconnect(self) -> None: ...
    def begin(self) -> None: ...
    def commit(self) -> None: ...
    def revert(self) -> None: ...
    def on_transaction_complete(self) -> None: ...
    def rollback(self) -> None: ...
    def put(self, address: Address, data: dict[str, Any]) -> None: ...
    def query(self, address: Address, query_specifier: QuerySpecifier | None = ..., conditions: Q | None = ..., pagination: NumberPaginator | CursorPaginator | None = ..., order_by: list[OrderBy] | None = ...) -> list[dict[str, Any]]: ...
    def count(self, address: Address, conditions: Q | None = ...) -> int: ...
    def prepare_connection(self) -> None: ...
