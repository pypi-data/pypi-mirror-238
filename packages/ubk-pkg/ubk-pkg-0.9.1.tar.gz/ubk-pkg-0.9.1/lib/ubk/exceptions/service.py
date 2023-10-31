"""
custom exceptions
"""


class UBKServiceException(Exception):
    """
    UBKException custom exception.
    """
    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)
