from abc import ABC, abstractmethod
from typing import List, Dict, Union
from domain.model.value.ImdbId import ImdbId

class OmdbProviderPort(ABC):
    """
    Port interface for fetching movie data from an external provider (e.g. OMDb).
    """

    @abstractmethod
    def fetch_by_id(self, imdb_id: Union[ImdbId, str]) -> Dict:
        """
        Fetch full movie details by IMDb ID.
        Returns a raw dict that will be translated by the ACL translator.
        """
        raise NotImplementedError

    @abstractmethod
    def search(self, title: str, year: Union[int, None]) -> List[Dict]:
        """
        Search for movies by title and optional year.
        Returns a list of raw dicts to be translated by the ACL translator.
        """
        raise NotImplementedError
