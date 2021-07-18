import traceback

from datamodel.bank_transaction import BankTransaction
from exceptions.exceptions import UnloaderError
from unloader.base_unloader import BaseUnloader
from typing import List, Generator, TextIO
from csv import DictWriter
from dataclasses import asdict, fields


class CsvUnloader(BaseUnloader):
    """
    Unload data to csv format
    """

    def __init__(self, output_file_name: str):
        super().__init__()
        self.output_file_name = output_file_name

    def unload_iterative(self, bunk_trans_generators: List[Generator[BankTransaction, None, None]]) -> None:
        """
        Method uses when you need to reduce consumption of RAM
        :param bunk_trans_generators: List of generators with transactions that will be unloaded to csv file
        :return:
        """
        try:
            with open(self.output_file_name, 'w') as output_csv:
                writer = self._create_dict_writer(output_csv)
                for gen in bunk_trans_generators:
                    for transaction in gen:
                        writer.writerow(asdict(transaction))
        except FileNotFoundError as e:
            raise UnloaderError(message=f"Can't open {self.output_file_name}") from e

    def unload(self, bank_transactions: List[BankTransaction]) -> None:
        """
        Create csv file with data from list
        :param bank_transactions: List of transactions that will be unloaded to destination csv file
        :return: None
        """
        try:
            with open(self.output_file_name, 'w') as output_csv:
                writer = self._create_dict_writer(output_csv)
                for transaction in bank_transactions:
                    writer.writerow(asdict(transaction))
        except FileNotFoundError as ex:
            raise UnloaderError(message=f"Can't open  {self.output_file_name}, {traceback.format_exc()}") from ex

    def _create_dict_writer(self, output_csv: TextIO):
        fieldnames = [field.name for field in fields(BankTransaction)]
        writer = DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()
        return writer
