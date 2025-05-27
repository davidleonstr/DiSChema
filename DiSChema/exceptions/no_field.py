from typing import Callable, Optional

class NoFieldError(Exception):
    def __init__(
            self, 
            field: Optional[str], 
            message: Optional[str] = None
        ):
        self.field = field

        if message is None:
            message = no_field_msg(self.field)
            
        self.message = message
        super().__init__(message)
        
no_field_msg: Callable[[str], str] = \
    lambda field: f"The field '{field}' does not exist in the data"