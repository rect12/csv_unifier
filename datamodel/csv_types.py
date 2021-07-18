from enum import Enum
from typing import Optional
import re


class CsvType(Enum):
    """
    Enum with processed banks.
    Enum key is connected with bank file name.
    Based on this information we can decide how to parse csv file lines.
    """

    BANK_1 = re.compile(r'^bank_1.csv$')
    BANK_2 = re.compile(r'^bank_2.csv$')
    BANK_3 = re.compile(r'^bank_3.csv$')

    @classmethod
    def get_bank(cls, file_name: str) -> Optional['CsvType']:
        for csv_type in cls:
            if csv_type.value.match(file_name):
                return csv_type
        return None
