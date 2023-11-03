import unittest

from code_wallet.library.kin import Kin
from code_wallet.library.payload import CodePayload, CodeKind
from code_wallet.library.errors import ErrInvalidCurrency, ErrInvalidSize

class TestCodePayload(unittest.TestCase):

    nonce = bytes([
        0x01, 0x02, 0x03, 0x04, 0x05, 
        0x06, 0x07, 0x08, 0x09, 0x10, 
        0x11
    ])

    fiat_amount = 281474976710911
    kin_amount = Kin.from_quarks(5000000)

    sample_kin = bytes([
        0x00, 0x40, 0x4B, 0x4C, 0x00, 
        0x00, 0x00, 0x00, 0x00, 0x01, 
        0x02, 0x03, 0x04, 0x05, 0x06, 
        0x07, 0x08, 0x09, 0x10, 0x11
    ])

    sample_kin_as_fiat = bytes([
        0x02, 0x00, 0x88, 0x13, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x01,
        0x02, 0x03, 0x04, 0x05, 0x06,
        0x07, 0x08, 0x09, 0x10, 0x11
    ])

    sample_fiat = bytes([
        0x02, 0x8c, 0xFF, 0x00, 0x00, 
        0x00, 0x00, 0x00, 0x01, 0x01, 
        0x02, 0x03, 0x04, 0x05, 0x06, 
        0x07, 0x08, 0x09, 0x10, 0x11
    ])

    def test_create_new_payload_from_parameters(self):
        kind = CodeKind.Cash
        amount = 100
        payload = CodePayload(kind, amount, self.nonce)
        
        self.assertEqual(payload.kind, kind)
        self.assertEqual(payload.amount, amount)
        self.assertEqual(payload.nonce, self.nonce)

    def test_invalid_size(self):
        data = bytes(19) # Incorrect size
        with self.assertRaises(ErrInvalidSize):
            CodePayload.from_data(data)

    def test_serialize_deserialize_for_cash_giftcard(self):
        kind = CodeKind.Cash
        amount = 100
        payload = CodePayload(kind, amount, self.nonce)
        
        serialized = payload.to_binary()
        deserialized = CodePayload.from_data(serialized)

        self.assertEqual(deserialized.kind, kind)
        self.assertEqual(deserialized.amount, amount)
        self.assertEqual(deserialized.nonce, self.nonce)

    def test_serialize_deserialize_for_request_payment(self):
        kind = CodeKind.RequestPayment
        amount = 100
        currency = 'usd'

        payload = CodePayload(kind, amount, self.nonce, currency)

        serialized = payload.to_binary()
        deserialized = CodePayload.from_data(serialized)

        self.assertEqual(deserialized.kind, kind)
        self.assertEqual(deserialized.amount, amount)
        self.assertEqual(deserialized.nonce, self.nonce)
        self.assertEqual(deserialized.currency, currency)

    def test_invalid_currency(self):
        kind = CodeKind.RequestPayment
        amount = 100
        currency = 'INVALID' 

        with self.assertRaises(ErrInvalidCurrency):
            CodePayload(kind, amount, self.nonce, currency)

    def test_encode_kin_cash(self):
        amount = self.kin_amount.to_quarks()
        payload = CodePayload(CodeKind.Cash, amount, self.nonce)

        encoded = payload.to_binary()
        self.assertEqual(encoded, self.sample_kin)

    def test_encode_kin_request(self):
        amount = int(self.kin_amount.to_decimal() * 100)
        payload = CodePayload(CodeKind.RequestPayment, amount, self.nonce, 'kin')

        encoded = payload.to_binary()
        self.assertEqual(encoded, self.sample_kin_as_fiat)

    def test_encode_fiat(self):
        amount = self.fiat_amount
        payload = CodePayload(CodeKind.RequestPayment, amount, self.nonce, 'usd')

        encoded = payload.to_binary()
        self.assertEqual(encoded, self.sample_fiat)

if __name__ == "__main__":
    unittest.main()