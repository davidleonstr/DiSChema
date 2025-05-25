from typing import Callable

class InvalidTypeError(Exception):
    def __init__(self, message: str, code: int = 100):
        super().__init__(message, code)
        self.message = message
        self.code = code

invalid_type: Callable[[str, str], str] = lambda field, type: f"The field type of '{field}' is not {type}"
