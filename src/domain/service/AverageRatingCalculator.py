from typing import List
from domain.model.value.Rating import Rating

class AverageRatingCalculator:
    @staticmethod
    def compute(ratings: List[Rating]) -> float:
        """
        Compute the arithmetic mean of a list of Rating value objects.
        Returns 0.0 if the list is empty.
        """
        if not ratings:
            return 0.0
        total = sum(r.value for r in ratings)
        return total / len(ratings)
