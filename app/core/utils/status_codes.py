import httpx
from app.core.exceptions import (
    ProviderAuthenticationError,
    ProviderPaymentRequiredError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderUnavailableError,
)


def raise_for_status(response: httpx.Response) -> None:
    """
    Raise provider exception based on HTTP status code.
    """
    if response.status_code == 401:
        raise ProviderAuthenticationError()
    if response.status_code == 402:
        raise ProviderPaymentRequiredError()
    if response.status_code == 429:
        raise ProviderRateLimitError()
    if 500 <= response.status_code:
        raise ProviderUnavailableError()
    if response.status_code >= 400:
        raise ProviderResponseError(response.text)
