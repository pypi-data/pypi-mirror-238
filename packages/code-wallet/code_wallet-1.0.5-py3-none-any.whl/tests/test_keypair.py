import unittest
from base64 import b64decode
from code_wallet.library.keypair import Keypair

class TestKeypair(unittest.TestCase):

    def test_generate_new_keypair(self):
        keypair = Keypair.generate()
        self.assertEqual(len(keypair.get_private_value()), 32)
        self.assertEqual(len(keypair.get_public_value()), 32)

    def test_create_keypair_from_secret_key(self):
        secret_key = b64decode('mdqVWeFekT7pqy5T49+tV12jO0m+ESW7ki4zSU9JiCgbL0kJbj5dvQ/PqcDAzZLZqzshVEs01d1KZdmLh4uZIg==')
        keypair = Keypair.from_secret_key(secret_key)
        self.assertEqual(keypair.get_public_key().to_base58(), '2q7pyhPwAwZ3QMfZrnAbDhnh9mDUqycszcpf86VgQxhF')
        secret_key_string = ','.join(map(str, keypair.get_secret_key()))
        expected_secret = ('153,218,149,89,225,94,145,62,233,171,46,83,227,223,173,87,93,163,59,73,' 
                           '190,17,37,187,146,46,51,73,79,73,136,40,27,47,73,9,110,62,93,189,15,207,' 
                           '169,192,192,205,146,217,171,59,33,84,75,52,213,221,74,101,217,139,135,139,153,34')
        self.assertEqual(secret_key_string, expected_secret)

    def test_generate_keypair_from_random_seed(self):
        seed = bytes([8] * 32)
        keypair = Keypair.from_seed(seed)
        self.assertEqual(keypair.get_public_key().to_base58(), '2KW2XRd9kwqet15Aha2oK3tYvd3nWbTFH1MBiRAv1BE1')

if __name__ == "__main__":
    unittest.main()