import unittest
from contextlib import ExitStack
from dataclasses import fields

from bank_csv_reader.csv_reader import BankCsvReader
from datamodel.bank_transaction import BankTransaction
from exceptions.exceptions import UnloaderError
from unloader.base_unloader import BaseUnloader
from unloader.csv_unloader import CsvUnloader


def flatten(t):
    return [item for sublist in t for item in sublist]


class TestCsvUnloader(unittest.TestCase):

    def setUp(self) -> None:
        files = [
            "resources/bank_1.csv",
            "resources/bank_2.csv",
            "resources/bank_3.csv"
        ]

        self.dest_file = "resources/test_unified.csv"

        with ExitStack() as stack:
            self.records = flatten([stack.enter_context(BankCsvReader(fname)).readlines() for fname in files])

    def test_lines_amount_in_dest_file(self):
        unloader: BaseUnloader = CsvUnloader(self.dest_file)
        unloader.unload(self.records)
        rows_number = 0
        with open(self.dest_file, "r") as dest_file:
            for line in dest_file:
                if line != "\n":
                    rows_number += 1
        self.assertEqual(rows_number - 1, len(self.records))  # we count without header

    def test_header(self):
        with open(self.dest_file, "r") as dest_file:
            header = next(dest_file)
        self.assertEqual(header, ",".join([field.name for field in fields(BankTransaction)]) + "\n")

    def test_incorrect_dest_file(self):
        def unload_csv():
            unloader: BaseUnloader = CsvUnloader("not_existing_dir/unified_file.csv")
            unloader.unload(self.records)

        self.assertRaises(UnloaderError, unload_csv)
