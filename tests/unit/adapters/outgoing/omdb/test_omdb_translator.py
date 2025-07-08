import pytest
from adapters.outgoing.omdb.omdb_acl_translator import OmdbACLTranslator


# Test get_year_interpretation
@pytest.mark.parametrize("raw, expected", [
    ("2025", "2025"),
    ("Released in 2021", "2021"),
    ("Year 19841985", "1984"),
    ("No year", None),
    ("20", None),
    ("", None)
])
def test_get_year_interpretation(raw, expected):
    translator = OmdbACLTranslator()
    result = translator.get_year_interpretation(raw)
    assert result == expected


# Test attribute handlers
def test_handle_year():
    translator = OmdbACLTranslator()
    result = translator.handle_year("year", "Released in 1999")
    assert result == "1999"

    result = translator.handle_year("year", None)
    assert result is None

    result = translator.handle_year("year", "20")
    assert result is None


def test_handle_title():
    translator = OmdbACLTranslator()
    result = translator.handle_title("title", "Inception   ")
    assert result == "Inception"

    result = translator.handle_title("title", None)
    assert result is None


def test_attribute_fallback_handler():
    translator = OmdbACLTranslator()
    result = translator.fallback_handler("unsupported_attribute", "value")
    assert result is None


# Test process_attributes
def test_process_attributes():
    translator = OmdbACLTranslator()
    translator.register_handlers()

    raw_data = {
        "year": "Released in 1994",
        "title": " Pulp Fiction ",
        "unsupported": "This should be ignored"
    }
    result = translator.process_attributes(raw_data)

    assert result == {
        "year": "1994",
        "title": "Pulp Fiction"
    }


# Test OMDb to domain translation
def test_translate_omdb_to_domain_dict():
    translator = OmdbACLTranslator()
    translator.register_handlers()

    raw_data = {
        "imdb_id": "tt1234567",
        "title": " The Matrix ",
        "year": "1999",
        "genre": "Action, Sci-Fi",
        "director": "The Wachowskis",
        "actors": "Keanu Reeves, Laurence Fishburne",
        "imdb_rating": "8.7",
        "plot": "A hacker discovers reality is a simulation."
    }
    result = translator.translate_omdb_to_domain_dict(raw_data)

    assert result == {
        "imdb_id": "tt1234567",
        "title": "The Matrix",
        "year": "1999",
        "genre": "Action, Sci-Fi",
        "director": "The Wachowskis",
        "actors": "Keanu Reeves, Laurence Fishburne",
        "imdb_rating": "8.7",
        "plot": "A hacker discovers reality is a simulation."
    }