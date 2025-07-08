from abc import ABC, abstractmethod
from typing import List, Union
from domain.model.value.ImdbId import ImdbId
from domain.model.Review import Review

class ReviewRepositoryPort(ABC):
    """
    Port interface for persisting and retrieving Review entities.
    """

    @abstractmethod
    def save(self, review: Review) -> None:
        """
        Persist a new Review.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_imdb(self, imdb_id: Union[ImdbId, str]) -> List[Review]:
        """
        Retrieve all reviews for the given IMDb identifier,
        ordered by creation time (e.g., most recent first).
        """
        raise NotImplementedError
