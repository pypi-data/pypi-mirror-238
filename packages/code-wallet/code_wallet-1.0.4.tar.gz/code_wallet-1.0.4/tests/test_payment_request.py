import unittest

from code_wallet.library.payment_request import PaymentRequestIntent
from code_wallet.library.errors import (
    ErrAmountRequired,
    ErrCurrencyRequired,
    ErrDestinationRequired,
    ErrInvalidCurrency
)

class TestPaymentRequestIntent(unittest.TestCase):

    def setUp(self):
        self.destination = '11111111111111111111111111111111'

    def test_constructor(self):
        intent = PaymentRequestIntent({
            'destination': self.destination,
            'amount': 10,
            'currency': 'kin'
        })

        self.assertEqual(intent.options['destination'], self.destination)
        self.assertEqual(intent.options['amount'], 10)
        self.assertEqual(intent.options['currency'], 'kin')
        self.assertEqual(intent.convertedAmount, 10 * 100)

        intent2 = PaymentRequestIntent({
            'destination': self.destination,
            'amount': 10,
            'currency': 'usd'
        })

        self.assertEqual(intent2.options['destination'], self.destination)
        self.assertEqual(intent2.options['amount'], 10)
        self.assertEqual(intent2.options['currency'], 'usd')
        self.assertEqual(intent2.convertedAmount, 10 * 100)

    def test_validate(self):
        with self.assertRaises(ErrDestinationRequired):
            PaymentRequestIntent({
                'amount': 10,
                'currency': 'kin'
            })

        with self.assertRaises(ErrAmountRequired):
            PaymentRequestIntent({
                'destination': self.destination,
                'currency': 'kin'
            })

        with self.assertRaises(ErrCurrencyRequired):
            PaymentRequestIntent({
                'destination': self.destination,
                'amount': 10,
            })

        with self.assertRaises(ErrInvalidCurrency):
            PaymentRequestIntent({
                'destination': self.destination,
                'amount': 10,
                'currency': 'invalidCurrency'
            })

    def test_sign(self):
        intent = PaymentRequestIntent({
            'destination': self.destination,
            'amount': 10,
            'currency': 'usd',
            'idempotencyKey': '1234'
        })

        actual = intent.sign()
        expected = {
            'message': bytearray([
                10, 34, 10, 32,  0,  0,  0,   0,   0,   0,  0,
                0,  0,  0,  0,  0,  0,  0,   0,   0,   0,  0,
                0,  0,  0,  0,  0,  0,  0,   0,   0,   0,  0,
                0,  0,  0, 26, 14, 10,  3, 117, 115, 100, 17,
                0,  0,  0,  0,  0,  0, 36,  64
            ]),
            'intent': 'GHEXGTE2r1PartuDip4VhDz8b2RY4xqRTRtMCUEaEXXN',
            'signature': bytearray([
                103, 103, 195, 242,   9,  66, 226,  48,  98, 182,  94,
                172, 255,  84, 166,  93, 138, 175, 245, 162, 121,  68,
                236,  16, 142,  46, 221, 160, 161,  70, 224,  49,  50,
                66,  74,  43, 247,  39,  69, 179, 130,  15, 140, 178,
                59, 255,  47, 104,  56,  75,  75, 193, 226,   2, 251,
                52, 183,   8,  41, 236, 218, 205,  21,  14
            ])
        }

        self.assertEqual(actual['intent'], expected['intent'])
        self.assertEqual(actual['message'], expected['message'])
        self.assertEqual(actual['signature'], expected['signature'])

if __name__ == "__main__":
    unittest.main()