from app.core.exceptions import (
    ProviderAuthenticationError,
    ProviderConfigurationError,
    ProviderError,
    ProviderPaymentRequiredError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderUnavailableError,
    XAccountNotFoundError,
)
from fastapi import Request, status
from fastapi.responses import JSONResponse

PROVIDER_ERROR_STATUS_MAP = {
    XAccountNotFoundError: status.HTTP_404_NOT_FOUND,
    ProviderConfigurationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    ProviderAuthenticationError: status.HTTP_401_UNAUTHORIZED,
    ProviderPaymentRequiredError: status.HTTP_402_PAYMENT_REQUIRED,
    ProviderRateLimitError: status.HTTP_429_TOO_MANY_REQUESTS,
    ProviderUnavailableError: status.HTTP_503_SERVICE_UNAVAILABLE,
    ProviderResponseError: status.HTTP_502_BAD_GATEWAY,
}


def _get_provider_error_status_code(exc: ProviderError) -> int:
    """
    Get HTTP status code for provider exception.
    """
    return PROVIDER_ERROR_STATUS_MAP.get(
        type(exc),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def provider_exception_handler(
    request: Request,
    exc: ProviderError,
) -> JSONResponse:
    """
    Convert provider errors into HTTP responses.
    """
    status_code = _get_provider_error_status_code(exc)
    return JSONResponse(status_code=status_code, content={"detail": exc.message})
