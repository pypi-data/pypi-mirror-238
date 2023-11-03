import abc
from abc import ABC, abstractmethod
from amsdal_data.operations.enums import OperationType as OperationType
from amsdal_data.transactions.manager import AmsdalTransactionManager as AmsdalTransactionManager
from amsdal_utils.models.base import ModelBase
from typing import TypeVar

ModelClass = TypeVar('ModelClass', bound=ModelBase)

class OperationsManagerBase(ABC, metaclass=abc.ABCMeta):
    def __init__(self, transaction_manager: AmsdalTransactionManager) -> None: ...
    @abstractmethod
    def perform_operation(self, obj: ModelClass, operation: OperationType) -> None: ...
