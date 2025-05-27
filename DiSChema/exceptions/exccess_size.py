from typing import Callable, Optional

class ExcessSizeError(Exception):
    def __init__(
            self, 
            field: Optional[str], 
            message: Optional[str] = None
        ):
        self.field = field

        if message is None:
            message = exccess_size_msg(self.field)
            
        self.message = message
        super().__init__(message)
        
exccess_size_msg: Callable[[str], str] = \
    lambda field: f"The field '{field}' exceeds the maximum size"