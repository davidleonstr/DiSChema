from typing import Callable, Optional

class MissingSizeError(Exception):
    def __init__(
            self, 
            field: Optional[str], 
            message: Optional[str] = None
        ):
        self.field = field

        if message is None:
            message = missing_size_msg(self.field)
            
        self.message = message
        super().__init__(message)

missing_size_msg: Callable[[str], str] = \
    lambda field: f"The field '{field}' is below the minimum size"