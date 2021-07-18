from typing import Optional

from bank_csv_reader.transaction_converter import convert_to_bank_transaction
from datamodel.bank_transaction import BankTransaction
from datamodel.csv_types import CsvType

from csv import DictReader
from pathlib import Path
from typing import List

from exceptions.exceptions import UnknownBankType


class BankCsvReader:
    """
    Class for reading csv files from banks and parsing them to
    uniform internal representation BankTransaction
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def __enter__(self):
        self.file = open(self.file_path, 'r')
        self.csv = DictReader(self.file)
        return self

    def __exit__(self, type, value, traceback):
        self.file.close()

    def __iter__(self):
        bank_type: Optional[CsvType] = CsvType.get_bank(Path(self.file_path).name)
        if bank_type is None:
            raise UnknownBankType("Unknown bank, can't understand how it will need to be processed")
        for line in self.csv.__iter__():
            yield convert_to_bank_transaction(line, bank_type)

    def readlines(self) -> List[BankTransaction]:
        """
        method returns all lines from input csv
        :return: List with converted to internal unified transaction type values
        """
        return [line for line in self]

