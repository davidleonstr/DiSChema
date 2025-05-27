from typing import Callable, Optional

class InvalidAllowedTypesError(Exception):
    def __init__(
            self, 
            field: Optional[str],
            position: Optional[int],
            message: Optional[str] = None
        ):
        self.field = field
        self.position = position

        if message is None:
            message = invalid_allowed_types_msg(self.field, self.position)
            
        self.message = message
        super().__init__(message)

invalid_allowed_types_msg: Callable[[str, str], str] = \
    lambda field, position: f"Invalid type in field '{field}'[{position}]"