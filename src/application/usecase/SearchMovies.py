from typing import Callable, Dict, List
import logging

from domain.model.MovieAggregate import MovieAggregate
from domain.port.repository.ReviewRepositoryPort import ReviewRepositoryPort
from application.dto.MovieSearchResponse import MovieSearchResponse, ReviewDto


class SearchMovies:
    """
    Use-case: perform a movie search via one of multiple strategies,
    enrich each result with user reviews, and return search DTOs.
    """

    def __init__(
            self,
            review_repo: ReviewRepositoryPort,
            translator: Callable[[dict], 'MovieAggregate'],
            strategies: Dict[str, object]
    ):
        self.review_repo = review_repo
        self.translator = translator
        self.strategies = strategies
        self.logger = logging.getLogger(__name__)

    def execute(self, title: str, year: int | None) -> List[MovieSearchResponse]:
        key = "title_year" if year else "title_only"
        strategy = self.strategies.get(key)
        if not strategy:
            raise ValueError(f"No search strategy configured for '{key}'")

        self.logger.debug(f"Searching for movies with title: {title}" + (f" and year: {year}" if year else ""))

        raw_list = strategy.search(title, year)

        results: List[MovieSearchResponse] = []
        for raw in raw_list:
            movie = self.translator(raw)
            reviews = self.review_repo.find_by_imdb(movie.imdb_id.value)
            movie.attach_reviews(reviews)

            review_dtos = [
                ReviewDto(
                    user_opinion=r.user_opinion.value,
                    user_rating=r.user_rating.value
                )
                for r in movie.reviews
            ]

            results.append(
                MovieSearchResponse(
                    title=movie.title,
                    year=movie.year.value,
                    imdb_id=movie.imdb_id.value,
                    genre=movie.genre,
                    imdb_rating=movie.imdb_rating,
                    reviews=review_dtos
                )
            )

        return results
