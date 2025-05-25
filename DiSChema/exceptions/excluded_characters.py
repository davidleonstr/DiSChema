from typing import Callable

class ExcludedCharactersError(Exception):
    def __init__(self, message: str, code: int = 100):
        super().__init__(message, code)
        self.message = message
        self.code = code

excluded_characters: Callable[[str], str] = lambda field: f"There are excluded characters in '{field}'"