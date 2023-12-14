class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class DatabaseNotConnectedError(Error):
    """Exception raised for errors if database not connected.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
