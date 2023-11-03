import hashlib

from code_wallet.library.keypair import Keypair
from code_wallet.library.payload import CodePayload

def generate_rendezvous_keypair(payload: CodePayload) -> Keypair:
    return Keypair.from_seed(hashlib.sha256(payload.to_binary()).digest())
