import unittest
from code_wallet.library.publickey import PublicKey

class TestPublicKey(unittest.TestCase):

    def test_from_base58(self):
        base58_key = PublicKey.from_base58('CiDwVBFgWV9E5MvXWoLgnEgn2hK7rJikbvfWavzAQz3')
        expected_bytes = bytes([3] + [0] * 31)
        
        self.assertEqual(base58_key.to_bytes(), expected_bytes)

    def test_to_base58(self):
        key = PublicKey.from_base58('CiDwVBFgWV9E5MvXWoLgnEgn2hK7rJikbvfWavzAQz3')
        self.assertEqual(key.to_base58(), 'CiDwVBFgWV9E5MvXWoLgnEgn2hK7rJikbvfWavzAQz3')
        
        key2 = PublicKey.from_base58('11111111111111111111111111111111')
        self.assertEqual(key2.to_base58(), '11111111111111111111111111111111')

    def test_to_bytes(self):
        key = PublicKey.from_base58('CiDwVBFgWV9E5MvXWoLgnEgn2hK7rJikbvfWavzAQz3')
        self.assertEqual(len(key.to_bytes()), 32)
        self.assertEqual(key.to_base58(), 'CiDwVBFgWV9E5MvXWoLgnEgn2hK7rJikbvfWavzAQz3')
        
        key2 = PublicKey.from_base58('11111111111111111111111111111111')
        self.assertEqual(len(key2.to_bytes()), 32)
        self.assertEqual(key2.to_base58(), '11111111111111111111111111111111')


if __name__ == '__main__':
    unittest.main()