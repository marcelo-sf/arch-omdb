from typing import Union, List, Dict

from adapters.outgoing.omdb.search_strategies import TitleOnlyStrategy
from domain.model.value.ImdbId import ImdbId
from domain.port.provider.OmdbProviderPort import OmdbProviderPort


def test_title_only_calls_fetch_search(monkeypatch):
    calls = []

    class FakeOmdb(OmdbProviderPort):
        def fetch_by_id(self, imdb_id: Union[ImdbId, str]) -> Dict:
            return {
                "imdb_id": "tt123",
                "title": "Mock Title",
                "year": 2000,
                "genre": "Mock Genre",
                "director": "Mock Director",
                "actors": ["Actor 1", "Actor 2"],
                "imdb_rating": "5.0",
                "plot": "Mock plot"
            }

        def search(self, title: str, year: Union[int, None]) -> List[Dict]:
            calls.append({"s": title})
            return [{
                "imdb_id": "tt123",
                "title": title,
                "year": 2000
            }]

    strat = TitleOnlyStrategy(FakeOmdb())
    result = strat.search("X", None)
    assert calls == [{"s": "X"}]
    assert result == [{"imdb_id": "tt123", "title": "X", "year": 2000}]
