from typing import List, Generator

from datamodel.bank_transaction import BankTransaction
from unloader.base_unloader import BaseUnloader


class JsonUnloader(BaseUnloader):
    """
    Class for unloading unified data to json format.
    Not implemented yet.
    """

    def __init__(self, output_file_name: str):
        super().__init__()
        self.output_file_name = output_file_name

    def unload(self, bank_transactions: List[BankTransaction]) -> None:
        raise NotImplemented

    def unload_iterative(self, bunk_trans_generator: List[Generator[BankTransaction, None, None]]) -> None:
        raise NotImplemented
