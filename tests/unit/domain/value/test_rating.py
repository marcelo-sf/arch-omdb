import pytest
from domain.model.value.Rating import Rating

def test_rating_within_bounds():
    r = Rating(5)
    assert r.value == 5

@pytest.mark.parametrize("invalid", [0, 11, -1])
def test_rating_out_of_bounds_raises(invalid):
    with pytest.raises(ValueError):
        Rating(invalid)
