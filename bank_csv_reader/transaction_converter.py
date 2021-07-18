from datamodel.bank_transaction import BankTransaction
from typing import Dict
import datetime as dt
from datamodel.csv_types import CsvType
from exceptions.exceptions import ReaderConvertorError
import traceback


def _convert_for_bank_1(line: Dict) -> BankTransaction:
    return BankTransaction(
        dt.datetime.strptime(line['timestamp'], "%b %d %Y").date(),
        line['type'],
        line['amount'],
        line['from'],
        line['to']
    )


def _convert_for_bank_2(line: Dict) -> BankTransaction:
    return BankTransaction(
        dt.datetime.strptime(line['date'], "%d-%m-%Y").date(),
        line['transaction'],
        line['amounts'],
        line['from'],
        line['to']
    )


def _convert_for_bank_3(line: Dict) -> BankTransaction:
    return BankTransaction(
        dt.datetime.strptime(line['date_readable'], "%d %b %Y").date(),
        line['type'],
        int(line['euro']) + int(line['cents']) / 100,
        line['from'],
        line['to']
    )


converters = {
    CsvType.BANK_1: _convert_for_bank_1,
    CsvType.BANK_2: _convert_for_bank_2,
    CsvType.BANK_3: _convert_for_bank_3
}


def convert_to_bank_transaction(line: Dict, bank_type: CsvType) -> BankTransaction:
    converter = converters.get(bank_type)
    if converter is None:
        raise ReaderConvertorError(message="Unknown bank format, can't get converter")
    try:
        return converter(line)
    except Exception:
        raise ReaderConvertorError(message=f"Can't convert csv line to unified format."
                                   f" An error is {traceback.format_exc()}")
