import unittest
from datetime import date

from bank_csv_reader.csv_reader import BankCsvReader
from datamodel.bank_transaction import BankTransaction
from exceptions.exceptions import UnknownBankType, ReaderConvertorError


class TestCsvReader(unittest.TestCase):

    def setUp(self) -> None:
        self.file_list = [
            "resources/bank_1.csv",
            "resources/bank_2.csv",
            "resources/bank_3.csv"
        ]

        self.bank_1_data = [
            BankTransaction(date=date(2019, 10, 1), type='remove', amount='99.20', id_from='198', id_to='182'),
            BankTransaction(date=date(2019, 10, 2), type='add', amount='2000.10', id_from='188', id_to='198')
        ]

    def test_reading_all_lines_from_csv(self):
        for file_path in self.file_list:
            rows_count = 0
            with open(file_path) as f:
                for line in f:
                    if line != "\n":
                        rows_count += 1
            with BankCsvReader(file_path) as reader:
                data = reader.readlines()
            self.assertEqual(len(data), rows_count - 1)  # we don't count trailer

    def test_valid_type_of_return_value(self):
        for file_path in self.file_list:
            with BankCsvReader(file_path) as reader:
                data = reader.readlines()
                for d in data:
                    self.assertIsInstance(d, BankTransaction)

    def test_check_valid_data_in_bank_transaction(self):
        bank_1_file = self.file_list[0]
        with BankCsvReader(bank_1_file) as reader:
            data = reader.readlines()
        self.assertListEqual(data, self.bank_1_data)

    def test_exception_file_not_found(self):
        def read_from_csv():
            with BankCsvReader("resources/not_exist_file.csv") as reader:
                return reader.readlines()
        self.assertRaises(FileNotFoundError, read_from_csv)

    def test_file_from_unknown_bank(self):
        def read_from_csv():
            with BankCsvReader("resources/bank_4.csv") as reader:
                return reader.readlines()

        self.assertRaises(UnknownBankType, read_from_csv)

    def test_not_valid_header_in_file(self):
        def read_from_csv():
            with BankCsvReader("resources/not_valid/bank_1.csv") as reader:
                return reader.readlines()

        self.assertRaises(ReaderConvertorError, read_from_csv)

    def test_not_valid_data_in_file_line(self):
        """
        In this test we have a month = 40, that is not exist
        """
        def read_from_csv():
            with BankCsvReader("resources/not_valid/bank_2.csv") as reader:
                return reader.readlines()

        self.assertRaises(ReaderConvertorError, read_from_csv)
