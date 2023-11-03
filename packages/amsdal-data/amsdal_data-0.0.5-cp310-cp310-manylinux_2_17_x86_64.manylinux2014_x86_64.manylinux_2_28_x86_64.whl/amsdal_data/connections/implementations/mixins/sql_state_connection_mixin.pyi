from _typeshed import Incomplete
from amsdal_data.connections.errors import AmsdalConnectionError as AmsdalConnectionError
from amsdal_data.table_schemas.constants import PRIMARY_PARTITION_KEY as PRIMARY_PARTITION_KEY
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.query.data_models.filter import Filter as Filter
from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from amsdal_utils.query.data_models.query_specifier import QuerySpecifier as QuerySpecifier
from amsdal_utils.query.enums import Lookup
from collections.abc import Callable as Callable
from pydantic import BaseModel
from typing import Any, ClassVar

SUPPORTED_NESTED_FIELDS: Incomplete
ADDRESS_FIELD: str

class NoValue: ...

class SqlOperatorTemplate(BaseModel):
    build_statement: ClassVar[Callable[[Any, str, Any], str]]
    build_value: ClassVar[Callable[[Any, Any], Any]]
    template: str | Callable[[Any], str]
    value_template: str | None
    value_modifier: Callable[[Any], Any] | None
    def build_statement(self, field_name: str, value: Any) -> str: ...
    def build_value(self, value: Any) -> Any: ...

sql_operator_map: dict[Lookup, SqlOperatorTemplate]

class SqlStateConnectionMixin: ...
