from collections.abc import Callable as Callable
from enum import Enum
from pydantic import BaseModel
from typing import Any, ClassVar

class IcebergDataTypes(str, Enum):
    BOOLEAN: str
    INT: str
    LONG: str
    FLOAT: str
    DOUBLE: str
    DATE: str
    TIME: str
    TIMESTAMP: str
    STRING: str
    UUID: str
    BINARY: str
    STRUCT: str
    LIST: str
    MAP: str

class ComplexType(BaseModel):
    to_sql: ClassVar[Callable[..., str]]
    def to_sql(self) -> str: ...

class StructType(ComplexType):
    to_sql: ClassVar[Callable[..., str]]
    fields: dict[str, IcebergDataTypes | ComplexType]
    def to_sql(self) -> str: ...

class MapType(ComplexType):
    to_sql: ClassVar[Callable[..., str]]
    key_type: IcebergDataTypes
    value_type: IcebergDataTypes | ComplexType
    def to_sql(self) -> str: ...

class ListType(ComplexType):
    to_sql: ClassVar[Callable[..., str]]
    element_type: IcebergDataTypes | ComplexType
    def to_sql(self) -> str: ...

class IcebergTableColumn(BaseModel):
    to_sql: ClassVar[Callable[..., str]]
    cid: int
    name: str
    type: IcebergDataTypes | ComplexType
    notnull: int
    def to_sql(self) -> str: ...
    @property
    def type_sql(self) -> str: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...

class IcebergTableColumnsSchema(BaseModel):
    to_sql: ClassVar[Callable[..., str]]
    columns: list['IcebergTableColumn']
    def to_sql(self) -> str: ...
