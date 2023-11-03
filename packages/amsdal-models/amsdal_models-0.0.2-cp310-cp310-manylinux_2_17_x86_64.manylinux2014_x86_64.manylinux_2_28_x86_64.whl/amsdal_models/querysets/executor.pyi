import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from amsdal_data.connections.base import ConnectionBase as ConnectionBase
from amsdal_models.querysets.base_queryset import QuerySetBase as QuerySetBase
from typing import Any

logger: Incomplete
DEFAULT_DB_ALIAS: str
LAKEHOUSE_DB_ALIAS: str

class ExecutorBase(ABC, metaclass=abc.ABCMeta):
    queryset: QuerySetBase
    def __init__(self, queryset: QuerySetBase) -> None: ...
    @abstractmethod
    def query(self) -> list[dict[str, Any]]: ...
    @abstractmethod
    def count(self) -> int: ...

class Executor(ExecutorBase):
    def query(self) -> list[dict[str, Any]]: ...
    def count(self) -> int: ...
