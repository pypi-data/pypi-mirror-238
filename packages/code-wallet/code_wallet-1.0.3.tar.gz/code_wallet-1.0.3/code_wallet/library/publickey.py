import base58

class PublicKey:
    def __init__(self, public_key: bytes):
        self.public_key = public_key

    @classmethod
    def from_base58(cls, base58_encoded: str):
        return cls(base58.b58decode(base58_encoded))

    def to_bytes(self) -> bytes:
        return bytes(self.public_key)

    def to_base58(self) -> str:
        return base58.b58encode(self.public_key).decode()

    def __str__(self):
        return self.to_base58()