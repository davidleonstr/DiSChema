from typing import Callable

class MissingSizeError(Exception):
    def __init__(self, message: str, code: int = 100):
        super().__init__(message, code)
        self.message = message
        self.code = code

missing_size: Callable[[str], str] = lambda field: f"The field '{field}' is below the minimum size"