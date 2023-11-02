"""Base classes for custom exceptions used in project."""


class MLMBaseException(Exception):
    """Base exception for all custom exceptions."""

    pass


class ServerException(MLMBaseException):
    """Base exception for all server mlmanager exceptions."""

    pass


class RegistryException(MLMBaseException):
    """Base exception for all registry exceptions."""

    pass


class ClientException(MLMBaseException):
    """Base exception for all client-side specific exceptions."""

    pass


class PylintException(MLMBaseException):
    """Base exception for all errors within linter check."""

    def __init__(self, message):
        super().__init__("Pylint found errors in code of uploaded modules:\n" + message)
