"""add x_api_response table

Revision ID: fb8602f2bb1a
Revises:
Create Date: 2026-06-01 17:37:56.407169

"""

import sqlalchemy as sa
from alembic import op
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "fb8602f2bb1a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "x_api_response",
        sa.Column("endpoint", sa.String(), nullable=False),
        sa.Column("request_params", sa.JSON(), nullable=False),
        sa.Column("response_data", sa.JSON(), nullable=True),
        sa.Column("error_snapshot", sa.JSON(), nullable=True),
        sa.Column("response_metadata", sa.JSON(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("x_api_response")
