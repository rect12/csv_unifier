import decimal
from dataclasses import dataclass
from datetime import date

from datamodel.transaction_type import TransactionType


@dataclass
class BankTransaction:
    """
    Dataclass for storing banks information
    """
    date:     date
    type:     TransactionType
    amount:   decimal
    id_from:  int
    id_to:    int
