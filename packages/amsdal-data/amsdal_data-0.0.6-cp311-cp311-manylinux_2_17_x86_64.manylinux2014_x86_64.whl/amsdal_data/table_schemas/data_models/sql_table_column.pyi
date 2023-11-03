from collections.abc import Callable as Callable
from pydantic import BaseModel
from typing import Any, ClassVar

class SqlTableColumnsSchema(BaseModel):
    to_sql: ClassVar[Callable[..., str]]
    columns: list['SqlTableColumn']
    def to_sql(self) -> str: ...

class SqlTableColumn(BaseModel):
    to_sql: ClassVar[Callable[..., str]]
    cid: int
    name: str
    type: str
    notnull: int
    dflt_value: Any
    pk: int
    def to_sql(self) -> str: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...
