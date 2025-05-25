from typing import Callable

class ExcessSizeError(Exception):
    def __init__(self, message: str, code: int = 100):
        super().__init__(message, code)
        self.message = message
        self.code = code
        
exccess_size: Callable[[str], str] = lambda field: f"The field '{field}' exceeds the maximum size"