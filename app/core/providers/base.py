from abc import ABC, abstractmethod
from app.schemas.x_entities import XAccountInfoResult


class XProvider(ABC):
    """
    Base interface for X data providers.
    """

    @abstractmethod
    async def get_account_info(self, username: str) -> XAccountInfoResult:
        """
        Get normalized X account information.
        """
