from typing import Callable
from domain.port.repository.ReviewRepositoryPort import ReviewRepositoryPort
from domain.port.provider.OmdbProviderPort import OmdbProviderPort
from application.dto.MovieDetailsResponse import (
    MovieDetailsResponse,
    ReviewDto,
    ActorDto
)

class GetMovieDetails:
    """
    Use-case: fetch movie metadata from OMDb, attach all user reviews,
    and return a combined DTO.
    """

    def __init__(
        self,
        review_repo: ReviewRepositoryPort,
        omdb_provider: OmdbProviderPort,
        translator: Callable[[dict], 'MovieAggregate']
    ):
        self.review_repo = review_repo
        self.omdb_provider = omdb_provider
        self.translator = translator

    def execute(self, imdb_id: str) -> MovieDetailsResponse:
        # 1) Fetch raw OMDb data
        raw = self.omdb_provider.fetch_by_id(imdb_id)

        # 2) Translate to domain aggregate
        movie = self.translator(raw)

        # 3) Load user reviews and attach
        reviews = self.review_repo.find_by_imdb(imdb_id)
        movie.attach_reviews(reviews)

        # 4) Map to DTOs
        actor_dtos = [ActorDto(name=a) for a in movie.actors]
        review_dtos = [
            ReviewDto(
                user_opinion=r.user_opinion.value,
                user_rating=r.user_rating.value
            )
            for r in movie.reviews
        ]

        return MovieDetailsResponse(
            title=movie.title,
            year=movie.year.value,
            imdb_id=movie.imdb_id.value,
            genre=movie.genre,
            director=movie.director,
            actors=actor_dtos,
            imdb_rating=movie.imdb_rating,
            plot=movie.plot,
            reviews=review_dtos
        )
