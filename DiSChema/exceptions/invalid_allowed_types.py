from typing import Callable

class InvalidAllowedTypesError(Exception):
    def __init__(self, message: str, code: int = 100):
        super().__init__(message, code)
        self.message = message
        self.code = code

invalid_allowed_types: Callable[[str, str], str] = lambda field, position: f"Invalid type in field '{field}'[{position}]"