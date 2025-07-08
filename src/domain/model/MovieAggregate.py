from datetime import datetime, timezone
from typing import List
from domain.model.value.ImdbId import ImdbId
from domain.model.value.Year import Year
from domain.model.Review import Review

class MovieAggregate:
    def __init__(self,
                 imdb_id,
                 title: str,
                 year,
                 genre: str,
                 director: str,
                 actors: List[str],
                 imdb_rating: str,
                 plot: str):
        # Value objects
        self.imdb_id = imdb_id if isinstance(imdb_id, ImdbId) else ImdbId(imdb_id)
        self.title = title
        self.year = year if isinstance(year, Year) else Year(year)
        self.genre = genre
        self.director = director
        self.actors = actors[:]  # list of strings
        self.imdb_rating = imdb_rating
        self.plot = plot

        self.reviews: List[Review] = []
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def attach_reviews(self, reviews: List[Review]):
        # Validate matching imdb_id
        for rev in reviews:
            if rev.imdb_id.value != self.imdb_id.value:
                raise ValueError(
                    f"Review imdb_id {rev.imdb_id.value} does not match MovieAggregate {self.imdb_id.value}"
                )
        self.reviews = reviews[:]
        self.updated_at = datetime.now(timezone.utc)

    def add_review(self, review: Review):
        if review.imdb_id.value != self.imdb_id.value:
            raise ValueError("Cannot add review with mismatched imdb_id")
        self.reviews.append(review)
        self.updated_at = datetime.now(timezone.utc)

    def __repr__(self):
        return (
            f"MovieAggregate(imdb_id={self.imdb_id}, title={self.title!r}, "
            f"year={self.year}, reviews={len(self.reviews)})"
        )
