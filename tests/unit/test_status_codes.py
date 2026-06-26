import httpx
import pytest
from app.core.exceptions import (
    ProviderAuthenticationError,
    ProviderPaymentRequiredError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderUnavailableError,
)
from app.core.utils.status_codes import raise_for_status


@pytest.mark.unit
class TestRaiseForStatus:
    """
    Tests for raise_for_status HTTP status code mapping.
    """

    @pytest.mark.parametrize(
        ("status_code", "expected_exc"),
        [
            (401, ProviderAuthenticationError),
            (402, ProviderPaymentRequiredError),
            (429, ProviderRateLimitError),
            (500, ProviderUnavailableError),
            (503, ProviderUnavailableError),
            (400, ProviderResponseError),
            (404, ProviderResponseError),
        ],
    )
    def test_raises_correct_exception_for_status_code(self, status_code, expected_exc):
        response = httpx.Response(status_code, text="error")

        with pytest.raises(expected_exc):
            raise_for_status(response)

    def test_does_not_raise_on_success(self):
        response = httpx.Response(200)

        raise_for_status(response)
