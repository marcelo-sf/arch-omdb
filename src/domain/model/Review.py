from datetime import datetime, timezone
from domain.model.value.ImdbId import ImdbId
from domain.model.value.OpinionText import OpinionText
from domain.model.value.Rating import Rating

class Review:
    def __init__(self, imdb_id, user_opinion, user_rating):
        try:
            self.imdb_id = imdb_id if isinstance(imdb_id, ImdbId) else ImdbId(imdb_id)
        except ValueError as e:
            raise ValueError(f"Invalid ImdbId: {imdb_id}") from e
        self.user_opinion = (
            user_opinion
            if isinstance(user_opinion, OpinionText)
            else OpinionText(user_opinion)
        )
        self.user_rating = (
            user_rating
            if isinstance(user_rating, Rating)
            else Rating(user_rating)
        )
        self.created_at = datetime.now(timezone.utc)

    def __eq__(self, other):
        """
        note: by design does not consider created_at as relevant for comparison purposes
        """
        return (
            isinstance(other, Review) and
            self.imdb_id == other.imdb_id and
            self.user_opinion == other.user_opinion and
            self.user_rating == other.user_rating
        )

    def __repr__(self):
        return (
            f"Review(imdb_id={repr(self.imdb_id)}, "
            f"opinion={repr(self.user_opinion)}, rating={repr(self.user_rating)})"
        )