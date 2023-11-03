import base58
import hashlib

from code_wallet.library.keypair import Keypair
from code_wallet.library.errors import ErrInvalidSize

class IdempotencyKey:
    MAX_LENGTH = 11

    def __init__(self, data=None):
        if data is None:
            data = bytearray(self.MAX_LENGTH)

        if len(data) != self.MAX_LENGTH:
            raise ErrInvalidSize()

        self.value = data

    @staticmethod
    def from_client_secret(data: str):
        return IdempotencyKey(base58.b58decode(data))

    @staticmethod
    def from_seed(seed: str):
        # Not ideal, an 11-byte hashing function is needed, and no such function exists
        hashed_seed = hashlib.sha256(seed.encode()).digest()
        return IdempotencyKey(hashed_seed[:IdempotencyKey.MAX_LENGTH])

    @staticmethod
    def generate():
        seed = Keypair.generate().private_key[:IdempotencyKey.MAX_LENGTH]
        return IdempotencyKey(seed)

    def __str__(self):
        return base58.b58encode(self.value).decode('utf-8')