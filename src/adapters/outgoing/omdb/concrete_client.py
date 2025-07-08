from tenacity import retry, stop_after_attempt
import random
import requests
from config.settings import Settings
from adapters.outgoing.omdb.abstract_client import AbstractOmdbClient
from domain.port.provider.OmdbProviderPort import OmdbProviderPort
from adapters.outgoing.omdb.omdb_acl_translator import OmdbACLTranslator

settings = Settings()


class OmdbClient(AbstractOmdbClient, OmdbProviderPort):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self._translator = OmdbACLTranslator()
        self._translator.register_handlers()

        self.backoff_base = settings.backoff_base
        self.backoff_cap = settings.backoff_cap
        self.retry_attempts = settings.retry_attempts

    # Retry logic using tenacity is using Decorrelated jitter.
    @retry(
        stop=stop_after_attempt(settings.retry_attempts),
        wait=lambda retry_state: min(
            float(settings.backoff_cap), random.uniform(settings.backoff_base, retry_state.seconds_since_start * 3)
        ),
        reraise=True,
    )
    def _get_with_retry(self, params: dict):
        resp = requests.get(self.BASE_URL, params=params, timeout=5)
        self._handle_http_errors(resp)
        return resp

    def _parse(self, raw: dict) -> dict:
        """
        Parses raw data from OMDb API into a domain dictionary.
        """
        actors_field = raw["Actors"]
        actors = [a.strip() for a in actors_field.split(",")]

        return self._translator.translate_omdb_to_domain_dict({
            "imdb_id": raw["imdbID"],
            "title": raw["Title"],
            "year": raw["Year"],
            "genre": raw["Genre"],
            "director": raw["Director"],
            "actors": actors,
            "imdb_rating": raw["imdbRating"],
            "plot": raw["Plot"],
        })

    def search(self, title: str, year: int | None) -> list[dict]:
        params = {"s": title, "apikey": self.api_key}
        if year is not None:
            params["y"] = year

        resp = self._get_with_retry(params)
        raw = resp.json()

        if raw.get("Response", "False") == "False":
            return []

        entries = raw.get("Search", [])
        results = []
        for item in entries:
            imdb_id = item.get("imdbID")
            if imdb_id:
                detail = self.fetch_by_id(imdb_id)
                results.append(detail)
        return results
