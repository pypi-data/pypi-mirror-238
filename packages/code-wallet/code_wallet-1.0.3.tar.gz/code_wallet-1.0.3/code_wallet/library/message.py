from typing import Union

from code_wallet.library.publickey import PublicKey

class ProtoMessage:
    def serialize(self) -> bytes:
        raise NotImplementedError

    @staticmethod
    def varint_encode(number: int) -> bytes:
        """Helper function to encode a number into varint format."""
        parts = []
        while number > 0x7F:
            parts.append((number & 0x7F) | 0x80)
            number >>= 7
        parts.append(number)
        return bytes(parts)

    @staticmethod
    def double_encode(number: float) -> bytes:
        """Helper function to encode a float into protobuf's double format."""
        import struct
        return struct.pack('<d', number)


class SolanaAccountId(ProtoMessage):
    def __init__(self, value: bytes):
        self.value = value

    def serialize(self) -> bytes:
        # Inner value prefix: Field=1, WireType=2 (length-delimited)
        value_serialized = b'\x0A' + ProtoMessage.varint_encode(len(self.value)) + self.value
        # Outer prefix: Field=1, WireType=2 (length-delimited)
        return b'\x0A' + ProtoMessage.varint_encode(len(value_serialized)) + value_serialized


class ExchangeData(ProtoMessage):
    def __init__(self, currency: str, rate: float, quarks: int, nativeAmount: float):
        self.currency = currency
        self.rate = rate
        self.quarks = quarks
        self.nativeAmount = nativeAmount

    def serialize(self) -> bytes:
        # currency: Field=1, WireType=2
        currency_bytes = self.currency.encode()
        serialized = b'\x0A' + ProtoMessage.varint_encode(len(currency_bytes)) + currency_bytes
        # exchange_rate: Field=2, WireType=1 (fixed 64-bit)
        serialized += b'\x11' + ProtoMessage.double_encode(self.rate)
        # native_amount: Field=3, WireType=1 (fixed 64-bit)
        serialized += b'\x19' + ProtoMessage.double_encode(self.nativeAmount)
        # quarks: Field=4, WireType=0 (varint)
        serialized += b'\x20' + ProtoMessage.varint_encode(self.quarks)
        return serialized


class ExchangeDataWithoutRate(ProtoMessage):
    def __init__(self, currency: str, nativeAmount: float):
        self.currency = currency
        self.nativeAmount = nativeAmount

    def serialize(self) -> bytes:
        # currency: Field=1, WireType=2
        currency_bytes = self.currency.encode()
        serialized = b'\x0A' + ProtoMessage.varint_encode(len(currency_bytes)) + currency_bytes
        # nativeAmount: Field=2, WireType=1 (fixed 64-bit)
        serialized += b'\x11' + ProtoMessage.double_encode(self.nativeAmount)
        return serialized


class RequestToReceiveBill(ProtoMessage):
    def __init__(self, requestorAccount: SolanaAccountId, exchangeData: Union[ExchangeData, ExchangeDataWithoutRate]):
        self.requestorAccount = requestorAccount
        self.exchangeData = exchangeData

    def serialize(self) -> bytes:
        serialized = self.requestorAccount.serialize()
        ed_bytes = self.exchangeData.serialize()

        # Decide on the prefix based on the type of exchangeData
        if isinstance(self.exchangeData, ExchangeData):
            serialized += b'\x12'  # Field=2, WireType=2
        else:
            serialized += b'\x1A'  # Field=3, WireType=2

        serialized += ProtoMessage.varint_encode(len(ed_bytes)) + ed_bytes
        return serialized


class Message(ProtoMessage):
    REQUEST_TO_RECEIVE_BILL_KIND = 5

    def __init__(self, value: RequestToReceiveBill):
        self.value = value

    def serialize(self) -> bytes:
        # Prefix for request_to_receive_bill: Field=5, WireType=2 (length-delimited)
        serialized_data = self.value.serialize()
        return b'\x2A' + ProtoMessage.varint_encode(len(serialized_data)) + serialized_data

