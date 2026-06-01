from app.core.database.base import Base
from app.models.mixins import IdMixin, TimestampMixin
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column


class XApiResponse(Base, IdMixin, TimestampMixin):
    """
    JSONB log of API responses and errors.
    """

    __tablename__ = "x_api_response"

    endpoint: Mapped[str]
    request_params: Mapped[dict] = mapped_column(JSON)
    response_data: Mapped[dict | None] = mapped_column(JSON)
    error_snapshot: Mapped[dict | None] = mapped_column(JSON)
    response_metadata: Mapped[dict | None] = mapped_column(JSON)
