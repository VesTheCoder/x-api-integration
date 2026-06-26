import pytest
from app.core.utils.pagination import cursor_pagination


@pytest.mark.unit
class TestCursorPagination:
    """
    Tests for cursor_pagination async generator.
    """

    async def test_yields_single_page_when_no_next_page(self):
        async def fetch_page(cursor):
            return {"data": [1, 2], "has_next_page": False}

        pages = [p async for p in cursor_pagination(fetch_page)]

        assert len(pages) == 1
        assert pages[0]["data"] == [1, 2]

    async def test_yields_multiple_pages_until_cursor_exhausted(self):
        async def fetch_page(cursor):
            if cursor is None:
                return {
                    "data": [1],
                    "has_next_page": True,
                    "next_cursor": "abc",
                }
            return {"data": [2], "has_next_page": False}

        pages = [p async for p in cursor_pagination(fetch_page)]

        assert len(pages) == 2
        assert pages[0]["data"] == [1]
        assert pages[1]["data"] == [2]

    async def test_stops_when_next_cursor_is_empty(self):
        async def fetch_page(cursor):
            return {"data": [1], "has_next_page": True, "next_cursor": ""}

        pages = [p async for p in cursor_pagination(fetch_page)]

        assert len(pages) == 1
