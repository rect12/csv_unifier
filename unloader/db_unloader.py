from typing import List, Generator

from datamodel.bank_transaction import BankTransaction
from unloader.base_unloader import BaseUnloader
from typing import io


class DbUnloader(BaseUnloader):
    """
    Class for unloading unified data to database.
    Not implemented yet.
    """

    def __init__(self, db_config: io):
        super().__init__()
        self.db_config = db_config

    def unload(self, bank_transactions: List[BankTransaction]) -> None:
        raise NotImplemented

    def unload_iterative(self, bunk_trans_generator: List[Generator[BankTransaction, None, None]]) -> None:
        raise NotImplemented
