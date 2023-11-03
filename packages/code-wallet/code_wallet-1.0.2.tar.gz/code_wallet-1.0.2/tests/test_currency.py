import unittest
from code_wallet.library.currency import currency_code_to_index, index_to_currency_code, is_valid_currency
from code_wallet.library.errors import ErrInvalidCurrency

class TestCurrencyUtilities(unittest.TestCase):

    def test_currency_code_to_index(self):
        self.assertEqual(currency_code_to_index("kin"), 0)
        self.assertEqual(currency_code_to_index("usd"), 140)
        self.assertEqual(currency_code_to_index("eur"), 43)

        with self.assertRaises(ErrInvalidCurrency):
            currency_code_to_index("invalid")

    def test_index_to_currency_code(self):
        self.assertEqual(index_to_currency_code(0), "kin")
        self.assertEqual(index_to_currency_code(140), "usd")
        self.assertEqual(index_to_currency_code(43), "eur")

        with self.assertRaises(ErrInvalidCurrency):
            index_to_currency_code(-1)
        with self.assertRaises(ErrInvalidCurrency):
            index_to_currency_code(200)  # 200 is out of bounds

    def test_is_valid_currency(self):
        self.assertTrue(is_valid_currency("kin"))
        self.assertTrue(is_valid_currency("usd"))
        self.assertTrue(is_valid_currency("eur"))
        
        self.assertFalse(is_valid_currency("invalid"))


if __name__ == '__main__':
    unittest.main()