from typing import Union, Dict, List
from adapters.outgoing.omdb.search_strategies import TitleYearStrategy
from domain.model.value.ImdbId import ImdbId
from domain.port.provider.OmdbProviderPort import OmdbProviderPort


def test_title_year_calls_fetch_search(monkeypatch):
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
            calls.append({"s": title, "y": year})
            return [{
                "imdb_id": "tt123",
                "title": title,
                "year": year or 2000
            }]

    strat = TitleYearStrategy(FakeOmdb())
    result = strat.search("X", 2021)
    assert calls == [{"s": "X", "y": 2021}]
    assert result == [{"imdb_id": "tt123", "title": "X", "year": 2021}]
