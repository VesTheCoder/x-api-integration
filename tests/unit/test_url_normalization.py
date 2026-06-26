import pytest
from app.core.utils import (
    normalize_single_tweet_id,
    normalize_tweet_ids,
    normalize_usernames,
)


@pytest.mark.unit
class TestNormalizeUsernames:
    """
    Tests for normalize_usernames utility function.
    """

    @pytest.mark.parametrize(
        ("values", "expected"),
        [
            (["elonmusk"], ["elonmusk"]),
            (["https://x.com/elonmusk"], ["elonmusk"]),
            (["https://x.com/elonmusk/"], ["elonmusk"]),
            (["elonmusk", "elonmusk"], ["elonmusk"]),
            ([""], []),
            (["elonmusk", "cnn"], ["elonmusk", "cnn"]),
            (["  elonmusk  "], ["elonmusk"]),
            (["https://x.com/elonmusk", "elonmusk"], ["elonmusk"]),
        ],
    )
    def test_normalize_usernames(self, values, expected):
        assert normalize_usernames(values) == expected


@pytest.mark.unit
class TestNormalizeTweetIds:
    """
    Tests for normalize_tweet_ids and normalize_single_tweet_id utility functions.
    """

    @pytest.mark.parametrize(
        ("values", "expected"),
        [
            (["123456789"], ["123456789"]),
            (["https://x.com/user/status/123456789"], ["123456789"]),
            (["123456789", "123456789"], ["123456789"]),
            (["not_a_url"], []),
            (["123456789", "987654321"], ["123456789", "987654321"]),
            ([""], []),
        ],
    )
    def test_normalize_tweet_ids(self, values, expected):
        assert normalize_tweet_ids(values) == expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("123456789", "123456789"),
            ("https://x.com/user/status/123456789", "123456789"),
            ("not_a_url", "not_a_url"),
            ("  123456789  ", "123456789"),
        ],
    )
    def test_normalize_single_tweet_id(self, value, expected):
        assert normalize_single_tweet_id(value) == expected
