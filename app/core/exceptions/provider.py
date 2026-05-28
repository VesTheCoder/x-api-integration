from app.core.exceptions.base import AppError
from enum import Enum


class ErrorCode(str, Enum):
    """
    Standardized error codes for provider operations.
    """

    RATE_LIMIT = 429
    PAYMENT_REQUIRED = 402
    INVALID_RESPONSE = 502
    UNAVAILABLE = 503


class ProviderError(AppError):
    """
    Base provider exception.
    """


class ProviderConfigurationError(ProviderError):
    """
    Raised when provider configuration is invalid.
    """

    def __init__(self, message: str = "Provider configuration is invalid") -> None:
        super().__init__(message)


class ProviderAuthenticationError(ProviderError):
    """
    Raised when provider rejects authentication.
    """

    def __init__(self, message: str = "Provider authentication failed") -> None:
        super().__init__(message)


class ProviderPaymentRequiredError(ProviderError):
    """
    Raised when provider balance or subscription is insufficient.
    """

    def __init__(self, message: str = "Provider payment required") -> None:
        super().__init__(message)


class ProviderRateLimitError(ProviderError):
    """
    Raised when provider rate limit is reached.
    """

    def __init__(self, message: str = "Provider rate limit reached") -> None:
        super().__init__(message)


class ProviderResponseError(ProviderError):
    """
    Raised when provider returns an invalid response.
    """

    def __init__(self, message: str = "Provider returned invalid response") -> None:
        super().__init__(message)


class ProviderUnavailableError(ProviderError):
    """
    Raised when provider is unavailable.
    """

    def __init__(self, message: str = "Provider is unavailable") -> None:
        super().__init__(message)
