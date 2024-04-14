from src.api._base import UnicornException


class RepositoryException(UnicornException):
    pass


class RepositoryNotFoundError(RepositoryException):
    pass
