from typing import Any, Dict, List, Optional
from domain.port.provider.OmdbProviderPort import OmdbProviderPort


class TitleOnlyStrategy:
    def __init__(self, client: OmdbProviderPort):
        self.client = client

    def search(self, title: str, year: Optional[int]) -> List[Dict[str, Any]]:
        return self.client.search(title, None)


class TitleYearStrategy:
    def __init__(self, client: OmdbProviderPort):
        self.client = client

    def search(self, title: str, year: Optional[int]) -> List[Dict[str, Any]]:
        return self.client.search(title, year)
