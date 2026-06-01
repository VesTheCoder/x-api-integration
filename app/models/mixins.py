import uuid
from datetime import datetime, timezone
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
    """
    Primary key UUID mixin for SQLAlchemy models.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )


class TimestampMixin:
    """
    Created-at timestamp mixin for SQLAlchemy models.
    """

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(timezone=timezone.utc),
    )
