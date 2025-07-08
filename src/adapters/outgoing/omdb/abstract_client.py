from abc import ABC, abstractmethod
import requests

class AbstractOmdbClient(ABC):
    BASE_URL = "http://www.omdbapi.com/"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_by_id(self, imdb_id: str) -> dict:
        url = f"{self.BASE_URL}?i={imdb_id}&apikey={self.api_key}"
        resp = requests.get(url, timeout=5)
        self._handle_http_errors(resp)
        raw = resp.json()
        self._handle_api_errors(raw)
        return self._parse(raw)

    def _handle_http_errors(self, resp: requests.Response):
        if resp.status_code != 200:
            raise ConnectionError(f"OMDb HTTP {resp.status_code}")

    def _handle_api_errors(self, raw: dict):
        if raw.get("Error"):
            raise ValueError(f"OMDb API Error: {raw['Error']}")

    @abstractmethod
    def _parse(self, raw: dict) -> dict:
        """Convert raw JSON → a minimal OmdbRawData dict"""
        ...

