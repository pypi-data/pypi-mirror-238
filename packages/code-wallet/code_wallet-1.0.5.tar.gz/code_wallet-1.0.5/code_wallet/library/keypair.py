from nacl import signing
from nacl.public import PublicKey as NaclPublicKey
from typing import Union

from code_wallet.library.publickey import PublicKey

class Keypair:
    def __init__(self, private_key: bytes, public_key: bytes):
        self.private_key = private_key
        self.public_key = public_key

    @classmethod
    def generate(cls):
        signer = signing.SigningKey.generate()
        return cls(signer._seed, signer.verify_key.encode())

    @classmethod
    def from_secret_key(cls, secret_key: bytes):
        private_key = secret_key[:32]
        signer = signing.SigningKey(private_key)
        return cls(private_key, signer.verify_key.encode())

    @classmethod
    def from_seed(cls, seed: bytes):
        return cls.from_secret_key(seed)

    @classmethod
    def from_raw_private_key(cls, raw_private_key: bytes):
        signer = signing.SigningKey(raw_private_key)
        return cls(raw_private_key, signer.verify_key.encode())

    def get_public_key(self):
        return PublicKey(self.public_key)

    def get_public_value(self):
        return self.public_key

    def get_private_value(self):
        return self.private_key

    def get_secret_key(self):
        return self.private_key + self.public_key

    def sign(self, message: Union[bytes, bytearray]) -> bytes:
        signer = signing.SigningKey(self.private_key)
        signed_message = signer.sign(message)
        return signed_message.signature

    def verify(self, message: Union[bytes, bytearray], signature: bytes) -> bool:
        verify_key = NaclPublicKey(self.public_key)
        try:
            verify_key.verify(signature + message)
            return True
        except:
            return False