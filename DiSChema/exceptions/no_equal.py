from typing import Callable, Optional

class NoEqualError(Exception):
    def __init__(
            self, 
            field: Optional[str], 
            equality: Optional[str], 
            message: Optional[str] = None
        ):
        self.field = field
        self.equality = equality

        if message is None:
            message = no_equal_msg(self.field, self.equality)
            
        self.message = message
        super().__init__(message)

no_equal_msg: Callable[[str, str], str] = \
    lambda field, equality: f"The field {field} is not equal of '{equality}'"