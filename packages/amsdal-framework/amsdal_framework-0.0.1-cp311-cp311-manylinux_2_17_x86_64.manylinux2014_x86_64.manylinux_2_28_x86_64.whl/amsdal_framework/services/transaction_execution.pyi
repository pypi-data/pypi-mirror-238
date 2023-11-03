from _typeshed import Incomplete
from amsdal_framework.configs.main import settings as settings
from amsdal_framework.errors import TransactionNotFoundError as TransactionNotFoundError
from amsdal_utils.utils.singleton import Singleton
from collections.abc import Callable as Callable
from typing import Any

logger: Incomplete

class TransactionExecutionService(metaclass=Singleton):
    _transactions: Incomplete
    def __init__(self) -> None: ...
    def execute_transaction(self, transaction_name: str, args: dict[str, Any]) -> Any: ...
    def get_transaction_func(self, transaction_name: str) -> Callable[..., Any]: ...
    @staticmethod
    def _run_async_transaction(transaction_func: Callable[..., Any], args: dict[str, Any]) -> Any: ...
