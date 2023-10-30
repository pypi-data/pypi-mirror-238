"""
 Copyright (C) 2023, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""


class BaseError(Exception):
    """
    Base class for creating custom exception classes.

    Attributes:
        message (str): Information about the error that occurred.
    """

    def __init__(self, message: str) -> None:
        """
        Initializes the BaseError object.

        Args:
            message (str): Information about the error that occurred.
        """
        self.message = message
        super().__init__()

    def __str__(self):
        """error message for exception"""
        return self.message


class ServerError(BaseError):
    """
    Custom exception class for handling errors that occur in server-related
    operations. This will capture all 5xx errors
    """


class UserError(BaseError):
    """
    Custom exception class for user-defined errors. This will capture
    all 4xx errors
    """


class InvalidAuthConfigError(UserError):
    """Custom exception class defined to handle errors raised
    due to Invalid api-key
    """


class ServerNotReachableError(BaseError):
    """Error thrown when the client is unable to connect to the server"""


class ErrorMessages:  # pylint: disable=too-few-public-methods
    """Class that that holds all error messages used in the sdk"""

    SDK_USER_ERR_01_INVALID_AUTH = "Invalid Authentication Config"
    SDK_SERVER_ERR_01_NOT_REACHABLE = "Server not reachable"
