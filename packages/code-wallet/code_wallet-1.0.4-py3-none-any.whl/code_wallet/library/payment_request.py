from code_wallet.library.publickey import PublicKey
from code_wallet.library.idempotency import IdempotencyKey
from code_wallet.library.payload import CodePayload, CodeKind
from code_wallet.library.rendezvous import generate_rendezvous_keypair
from code_wallet.library.message import (
    ExchangeData,
    ExchangeDataWithoutRate,
    RequestToReceiveBill,
    SolanaAccountId,
    Message
)
from code_wallet.library.errors import (
    ErrAmountRequired, 
    ErrCurrencyRequired, 
    ErrDestinationRequired, 
)

class PaymentRequestIntent:
    def __init__(self, opt: dict):
        self.options = {
            **opt,
            'currency': opt['currency'].lower() if opt.get('currency') else None
        }
        self.validate()

        if self.options.get('idempotencyKey'):
            self.nonce = IdempotencyKey.from_seed(self.options['idempotencyKey'])
        elif self.options.get('clientSecret'):
            self.nonce = IdempotencyKey.from_client_secret(self.options['clientSecret'])
        else:
            self.nonce = IdempotencyKey.generate()

        self.options['amount'] = round(float(self.options['amount']), 2)
        self.convertedAmount = int(round(self.options['amount'] * 100))

        kind = CodeKind.RequestPayment
        amount = self.convertedAmount
        nonce = self.nonce.value

        self.rendezvousPayload = CodePayload(kind, amount, nonce, self.options['currency'])
        self.rendezvousKeypair = generate_rendezvous_keypair(self.rendezvousPayload)

    def validate(self):
        if not self.options.get('destination'):
            raise ErrDestinationRequired()

        if not self.options.get('amount'):
            raise ErrAmountRequired()

        if not self.options.get('currency'):
            raise ErrCurrencyRequired()
    
    def to_msg(self):
        destination = PublicKey.from_base58(self.options['destination'])
        currency = self.options['currency']
        amount = self.options['amount']

        if currency == "kin":
            exchangeData = ExchangeData('kin', 1, self.convertedAmount, amount)
        else:
            exchangeData = ExchangeDataWithoutRate(currency, amount)

        requestorAccount = SolanaAccountId(destination.to_bytes())
        return RequestToReceiveBill(requestorAccount, exchangeData)

    def to_proto(self):
        return Message(self.to_msg()).serialize()

    def sign(self):
        msg = self.to_msg()
        envelope = self.to_proto()

        sig = self.rendezvousKeypair.sign(envelope)
        intent = self.rendezvousKeypair.get_public_key().to_base58()
        message = msg.serialize()
        signature = sig

        return {
            'message': message,
            'intent': intent,
            'signature': signature
        }

    def get_client_secret(self) -> str:
        return str(self.nonce)

    def get_intent_id(self) -> str:
        return self.rendezvousKeypair.get_public_key().to_base58()