class TwitterAPICostCalculator:
    """
    Calculates estimated cost for TwitterAPI.io requests.
    """

    COST_PER_ITEM_USD = 0.00015

    @classmethod
    def calculate(cls, item_count: int) -> float:
        """
        Calculate estimated cost in USD based on returned item count.
        Minimum cost is charged even when no items are returned.
        """
        return round(max(item_count, 1) * cls.COST_PER_ITEM_USD, 5)
