from contextlib import ExitStack

from bank_csv_reader.csv_reader import BankCsvReader
from unloader.base_unloader import BaseUnloader
from unloader.csv_unloader import CsvUnloader

import logging as log

log.basicConfig(filename="sample.log", level=log.INFO)


def flatten(t):
    return [item for sublist in t for item in sublist]


if __name__ == '__main__':
    files = ["test/resources/bank_1.csv", "test/resources/bank_2.csv", "test/resources/bank_3.csv"]
    dest_file = "unified.csv"
    log.info(f"Start process files {files}")

    with ExitStack() as stack:
        try:
            lines = flatten([stack.enter_context(BankCsvReader(fname)).readlines() for fname in files])
            log.info(f"Read {len(lines)} lines from all csv files")

            log.info("Unload lines to csv")
            unloader: BaseUnloader = CsvUnloader(dest_file)
            unloader.unload(lines)
        except Exception as ex:
            log.error(f"Exception occurred while reading from csv or unloading data")
            raise ex
