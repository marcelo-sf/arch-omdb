import pytest
from domain.model.value.Year import Year
import datetime

current_year = datetime.datetime.now().year

@pytest.mark.parametrize("valid", [current_year, 1900, 1999])
def test_year_valid(valid):
    y = Year(valid)
    assert y.value == valid

@pytest.mark.parametrize("invalid", [-1, 10000, "-2020"])
def test_year_invalid(invalid):
    with pytest.raises(ValueError):
        Year(invalid)

