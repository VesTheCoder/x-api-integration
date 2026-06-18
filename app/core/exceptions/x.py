from app.core.exceptions.base import AppError


class XAccountNotFoundError(AppError):
    """
    Raised when X account is not found.
    """

    def __init__(self, message: str = "X account not found") -> None:
        super().__init__(message)
