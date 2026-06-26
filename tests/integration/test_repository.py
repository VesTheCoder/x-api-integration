import pytest
from app.models.x_response import XApiResponse
from sqlalchemy import select
from tests.factories import x_api_response_log_factory


@pytest.mark.integration
class TestXApiResponseRepository:
    """
    Tests for XApiResponseRepository with in-memory SQLite.
    """

    async def test_create_log_persists_response_data(self, db_repo, db_session):
        kwargs = x_api_response_log_factory(
            response_data={"data": [{"id": "44196397"}]},
            error_snapshot=None,
        )
        await db_repo.create_log(**kwargs)

        result = await db_session.execute(select(XApiResponse))
        row = result.scalar_one()

        assert row.endpoint == "get_accounts_info"
        assert row.response_data == {"data": [{"id": "44196397"}]}
        assert row.response_metadata == {"latency_ms": 150}
        assert row.error_snapshot is None

    async def test_create_log_persists_error_snapshot(self, db_repo, db_session):
        kwargs = x_api_response_log_factory(
            response_data=None,
            error_snapshot={"error_code": 429, "error_message": "Rate limit"},
        )
        await db_repo.create_log(**kwargs)

        result = await db_session.execute(select(XApiResponse))
        row = result.scalar_one()

        assert row.error_snapshot == {"error_code": 429, "error_message": "Rate limit"}
        assert row.response_data is None
