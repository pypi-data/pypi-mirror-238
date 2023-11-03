from enum import Enum
from typing import Optional, List

from code_wallet.library.currency import CurrencyCode
from code_wallet.library.errors import ErrInvalidSize, ErrInvalidCurrency
from code_wallet.library.currency import currency_code_to_index, index_to_currency_code, is_valid_currency

# Enum representing types of code kinds.
class CodeKind(Enum):
    Cash = 0
    GiftCard = 1
    RequestPayment = 2

# CodePayload class represents the payload format for scan codes.
# It handles conversion to and from binary format and validation.
class CodePayload:
    MAX_LENGTH = 20

    def __init__(self, kind: CodeKind, amount: int, nonce: bytes, currency: Optional[CurrencyCode] = None):
        self.kind = kind
        self.amount = amount
        self.nonce = nonce

        # Validation for currency code
        if currency and not is_valid_currency(currency):
            raise ErrInvalidCurrency()
        self.currency = currency

    def to_binary(self) -> bytes:
        data = bytearray(20)
        data[0] = self.kind.value

        if self.kind == CodeKind.RequestPayment:
            # for Payment Request
            if not self.currency:
                raise ErrInvalidCurrency()
            
            currency_index = currency_code_to_index(self.currency)
            data[1] = currency_index
            for i in range(7):
                data[i + 2] = (self.amount >> (8 * i)) & 0xFF
        else:
            # for Cash and Gift Card
            for i in range(8):
                data[i + 1] = (self.amount >> (8 * i)) & 0xFF

        data[9:] = self.nonce
        
        return bytes(data)

    @staticmethod
    def from_data(data: bytes) -> 'CodePayload':
        if len(data) != CodePayload.MAX_LENGTH:
            raise ErrInvalidSize()

        type_ = CodeKind(data[0])
        amount = 0
        nonce = data[9:]
        currency = None

        if type_ == CodeKind.RequestPayment:
            # for Payment Request
            currency_index = data[1]
            currency = index_to_currency_code(currency_index)
            for i, val in enumerate(data[2:9]):
                amount += val << (8 * i)
        else:
            # for Cash and Gift Card
            for i, val in enumerate(data[1:9]):
                amount += val << (8 * i)
        
        return CodePayload(type_, amount, nonce, currency)
