import unittest
import base58

from code_wallet.library.idempotency import IdempotencyKey, ErrInvalidSize

class TestIdempotencyKey(unittest.TestCase):

    def test_create_idempotency_key_from_bytearray(self):
        key = IdempotencyKey()
        self.assertEqual(len(key.value), 11)

    def test_throw_err_invalid_size_for_bytearray(self):
        data = bytearray(10)  # Incorrect size
        with self.assertRaises(ErrInvalidSize):
            IdempotencyKey(data)

    def test_create_idempotency_key_from_client_secret(self):
        data = bytearray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        client_secret = base58.b58encode(data).decode('utf-8')
        key = IdempotencyKey.from_client_secret(client_secret)
        self.assertEqual(len(key.value), 11)
        self.assertEqual(key.value, base58.b58decode(client_secret))

    def test_create_idempotency_key_from_string(self):
        test_string = 'test_string'
        key = IdempotencyKey.from_seed(test_string)
        self.assertEqual(len(key.value), 11)

        expected_array = bytearray([
            0x4b, 0x64, 0x1e, 0x9a, 0x92,
            0x3d, 0x1e, 0xa5, 0x7e, 0x18,
            0xfe
        ])
        self.assertEqual(key.value, expected_array)

if __name__ == '__main__':
    unittest.main()