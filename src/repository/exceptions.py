from src.common.unicorn_exception import UnicornException


class RepositoryException(UnicornException):
    pass


class RepositoryNotFoundError(RepositoryException):
    pass


class RepositoryUnencryptedContentError(RepositoryException):
    """Content MUST be encrypted before being stored."""
