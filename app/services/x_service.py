from app.core.providers.base import XProvider
from app.schemas.x_entities import XAccountInfoResult


class XService:
    """
    Application service for X data operations.
    """

    def __init__(self, provider: XProvider) -> None:
        self.provider = provider

    async def get_account_info(self, username: str) -> XAccountInfoResult:
        """
        Get X account information by username.
        """
        return await self.provider.get_account_info(username)
