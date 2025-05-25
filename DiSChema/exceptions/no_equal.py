from typing import Callable

class NoEqualError(Exception):
    def __init__(self, message: str, code: int = 100):
        super().__init__(message, code)
        self.message = message
        self.code = code

no_equal: Callable[[str, str], str] = lambda field, equality: f"The field {field} is not equal of '{equality}'"