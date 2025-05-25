from typing import Callable

class NoFieldError(Exception):
    def __init__(self, message: str, code: int = 100):
        super().__init__(message, code)
        self.message = message
        self.code = code
        
no_field: Callable[[str], str] = lambda field: f"The field '{field}' does not exist in the data"