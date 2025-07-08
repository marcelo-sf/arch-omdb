import pytest
from domain.model.value.ImdbId import ImdbId

@pytest.mark.parametrize("valid", ["tt1234567", "tt0000001"])
def test_imdbid_valid(valid):
    id_obj = ImdbId(valid)
    assert id_obj.value == valid

@pytest.mark.parametrize("invalid", ["1234567", "ttABC", "tt", ""])
def test_imdbid_invalid(invalid):
    with pytest.raises(ValueError):
        ImdbId(invalid)

