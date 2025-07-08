from typing import List, Dict, Optional, Union
from domain.port.provider.OmdbProviderPort import OmdbProviderPort

class MockOmdbClient(OmdbProviderPort):
    """
    Mock implementation of OmdbProviderPort for tests
    """

    def fetch_by_id(self, imdb_id: Union[str, 'ImdbId']) -> Dict:
        iid = getattr(imdb_id, "value", imdb_id)
        return {
            "imdb_id": iid,
            "title":   f"Mock Title for {iid}",
            "year":    2000,
            "genre":   "MockGenre",
            "director":"Mock Director",
            "actors":  ["Actor One", "Actor Two"],
            "imdb_rating": "5.5",
            "plot":    f"This is a mock plot for {iid}."
        }

    def search(self, title: str, year: Optional[int]) -> List[Dict]:
        return [{
            "imdb_id": f"ttMOCK{abs(hash(title)) % 10000:04d}",
            "title":   f"Mock {title}",
            "year":    year or 2000,
            "genre":   "MockGenre",
            "director":"Mock Director",
            "actors":  ["Actor One", "Actor Two"],
            "imdb_rating": "5.5",
            "plot":    f"This is a mock plot for {title} ({year})."
        }]
