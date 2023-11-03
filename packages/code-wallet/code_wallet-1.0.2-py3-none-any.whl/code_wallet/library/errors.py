class ErrInvalidSize(Exception):
    """Raised when there is an invalid size."""
    def __init__(self):
        super().__init__("invalid size")


class ErrDestinationRequired(Exception):
    """Raised when a destination is required."""
    def __init__(self):
        super().__init__("destination is required")


class ErrAmountRequired(Exception):
    """Raised when an amount is required."""
    def __init__(self):
        super().__init__("amount is required")


class ErrCurrencyRequired(Exception):
    """Raised when a currency is required."""
    def __init__(self):
        super().__init__("currency is required")


class ErrInvalidCurrency(Exception):
    """Raised when there is an invalid currency."""
    def __init__(self):
        super().__init__("invalid currency")


class ErrUnexpectedError(Exception):
    """Raised when an unexpected error occurs."""
    def __init__(self):
        super().__init__("unexpected error")


class ErrAmbiguousNonce(Exception):
    """Raised when nonce cannot be derived from both clientSecret and idempotencyKey."""
    def __init__(self):
        super().__init__("cannot derive nonce from both clientSecret and idempotencyKey")


class ErrInvalidMode(Exception):
    """Raised when there is an invalid mode."""
    def __init__(self):
        super().__init__("invalid mode")