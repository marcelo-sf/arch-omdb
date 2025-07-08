from adapters.outgoing.omdb.omdb_acl_translator import OmdbACLTranslator
from domain.model.value.ImdbId import ImdbId

def test_translator_maps_to_domain():
    translator = OmdbACLTranslator()
    translator.register_handlers()  # Register default handlers explicitly
    raw = {
        "imdb_id": "tt1784",
        "title": "T",
        "year": 2001,
        "genre": "G",
        "director": "D",
        "actors": ["A"],
        "imdb_rating": "7",
        "plot": "P"
    }
    movie = translator.translate_omdb_to_domain_type(raw)
    assert movie.imdb_id == ImdbId("tt1784")
    assert movie.title == "T"
    assert movie.plot == "P"