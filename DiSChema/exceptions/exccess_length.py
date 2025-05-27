from typing import Callable, Optional

class ExcessLengthError(Exception):
    def __init__(
            self, 
            field: Optional[str], 
            message: Optional[str] = None
        ):
        self.field = field

        if message is None:
            message = exccess_length_msg(self.field)
            
        self.message = message
        super().__init__(message)
        
exccess_length_msg: Callable[[str], str] = \
    lambda field: f"The field '{field}' exceeds the maximum length"