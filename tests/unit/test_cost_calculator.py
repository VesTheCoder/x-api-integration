import pytest
from app.core.utils import TwitterAPICostCalculator


@pytest.mark.unit
class TestTwitterAPICostCalculator:
    """
    Tests for TwitterAPICostCalculator.calculate.
    """

    @pytest.mark.parametrize(
        ("item_count", "expected_cost"),
        [
            (0, 0.00015),
            (1, 0.00015),
            (10, 0.0015),
            (100, 0.015),
        ],
    )
    def test_calculate_cost(self, item_count, expected_cost):
        cost = TwitterAPICostCalculator.calculate(item_count)
        assert cost == pytest.approx(expected_cost, rel=1e-3)
