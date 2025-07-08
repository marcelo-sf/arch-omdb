import pytest
from domain.service.AverageRatingCalculator import AverageRatingCalculator
from domain.model.value.Rating import Rating

def test_average_rating_empty():
    avg = AverageRatingCalculator.compute([])
    assert avg == 0

def test_average_rating_non_empty():
    ratings = [Rating(5), Rating(7), Rating(8)]
    avg = AverageRatingCalculator.compute(ratings)
    assert avg == pytest.approx((5 + 7 + 8) / 3)

