from abc import ABC, abstractmethod
from typing import List, Generator

from datamodel.bank_transaction import BankTransaction


# todo:rename to unloader
class BaseUnloader(ABC):
    """
    Base class for unloaders. All unloaders should inherit from this one
    """
    @abstractmethod
    def unload(self, bank_transactions: List[BankTransaction]) -> None:
        pass

    @abstractmethod
    def unload_iterative(self, bunk_trans_generator: List[Generator[BankTransaction, None, None]]) -> None:
        pass
