[![pypi][pypi-image]][pypi-url]

[pypi-image]: https://img.shields.io/pypi/v/code-wallet.svg?style=flat
[pypi-url]: https://pypi.org/project/code-wallet/

# Code Wallet Python SDK

The Code Wallet Python SDK is a module that allows Python developers to integrate Code into their applications. Seamlessly start accepting payments with minimal setup and just a few lines of code.

See the [documentation](https://code-wallet.github.io/code-sdk/docs/guide/introduction.html) for more details.

## What is Code?

[Code](https://getcode.com) is a mobile wallet app leveraging self-custodial blockchain technology to provide an instant, global, and private payments experience.

## Installation

You can install the Code Wallet Python SDK from PyPI:

```bash
pip install code-wallet
```

## Usage
Here's a simple example showcasing how to create a payment intent using the Python SDK:

```python
from code_wallet.client.intents import payment_intents

test_data = {
    'destination': "E8otxw1CVX9bfyddKu3ZB3BVLa4VVF9J7CTPdnUwT9jR",
    'amount': 0.05,
    'currency': 'usd',
}

# Create a payment request intent
payment_intents.create(test_data)

# Verify the intent status
payment_intents.get_status(id)
```

## Getting Help

If you have any questions or need help integrating Code into your website or application, please reach out to us on [Discord](https://discord.gg/DunN9aNS) or [Twitter](https://twitter.com/getcode).

##  Contributing

For now the best way to contribute is to share feedback on [Discord](https://discord.gg/DunN9aNS). This will evolve as we continue to build out the platform and open up more ways to contribute. 
