import unittest

from code_wallet.client.intents import payment_intents
from code_wallet.library.payment_request import PaymentRequestIntent

class TestPaymentIntents(unittest.TestCase):

    def test_create(self):
        test_data = {
            'destination': "E8otxw1CVX9bfyddKu3ZB3BVLa4VVF9J7CTPdnUwT9jR",
            'amount': 0.05,
            'currency': 'usd',
        }

        response = payment_intents.create(test_data)

        test_data["clientSecret"] = response['clientSecret']
        expected_intent = PaymentRequestIntent(test_data)

        # Verifying both have the same id
        self.assertEqual(response['id'], expected_intent.get_intent_id())

if __name__ == '__main__':
    unittest.main()