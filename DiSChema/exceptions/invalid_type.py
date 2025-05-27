from typing import Callable, Optional

class InvalidTypeError(Exception):
    def __init__(
            self, 
            field: Optional[str], 
            type: Optional[str], 
            message: Optional[str] = None
        ):
        self.field = field
        self.type = type

        if message is None:
            message = invalid_type_msg(self.field, self.type)
            
        self.message = message
        super().__init__(message)

invalid_type_msg: Callable[[str, str], str] = \
    lambda field, type: f"The field type of '{field}' is not {type}"