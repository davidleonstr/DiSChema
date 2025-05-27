from typing import Callable, Optional

class ExcludedCharactersError(Exception):
    def __init__(
            self, 
            field: Optional[str], 
            message: Optional[str] = None
        ):
        self.field = field

        if message is None:
            message = excluded_characters_msg(self.field)
            
        self.message = message
        super().__init__(message)

excluded_characters_msg: Callable[[str], str] = \
    lambda field: f"There are excluded characters in '{field}'"