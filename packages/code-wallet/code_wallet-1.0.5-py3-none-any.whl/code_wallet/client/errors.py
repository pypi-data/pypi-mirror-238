class ErrUnexpectedError(Exception):
    def __init__(self):
        super().__init__("unexpected error")

class ErrUnexpectedHttpStatus(Exception):
    def __init__(self, val: any, msg: any):
        super().__init__(f"unexpected HTTP status: {val}, {msg}")

class ErrUnexpectedServerError(Exception):
    def __init__(self, val: any):
        super().__init__(f"unexpected server error: {val}")