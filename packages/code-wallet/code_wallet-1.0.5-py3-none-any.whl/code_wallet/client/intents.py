from enum import Enum
from typing import Any, Dict
import base64
import base58

from code_wallet.library.payment_request import PaymentRequestIntent
from code_wallet.client.connection import Connection

api = 'https://api.getcode.com/v1'
client = Connection(api)

class PaymentIntentState(Enum):
    Pending = 'pending'
    Confirmed = 'confirmed'

pending = {'status': PaymentIntentState.Pending.value}
confirmed = {'status': PaymentIntentState.Confirmed.value}

class PaymentIntents:

    @staticmethod
    def create(obj: Dict[str, Any]) -> Dict[str, str]:
        obj['mode'] = 'payment'

        intent = PaymentRequestIntent(obj)

        envelope = intent.sign()
        body = {
            'intent': envelope.get('intent'),
            'message': base64.urlsafe_b64encode(envelope.get('message')).decode('utf-8').rstrip('='),
            'signature': base58.b58encode(envelope.get('signature')).decode(),
            'webhook': obj.get('webhook', {}).get('url')
        }

        client.post('createIntent', body)

        return {
            'clientSecret': intent.get_client_secret(),
            'id': intent.get_intent_id()
        }

    @staticmethod
    def get_status(intent_id: str) -> Dict[str, str]:
        res = client.get('getStatus', {'intent': intent_id})

        if res['status'] == 'SUBMITTED':
            return confirmed

        return pending

payment_intents = PaymentIntents()