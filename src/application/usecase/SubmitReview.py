from domain.model.Review import Review
from domain.model.value.ImdbId import ImdbId
from domain.model.value.OpinionText import OpinionText
from domain.model.value.Rating import Rating
from domain.port.repository.ReviewRepositoryPort import ReviewRepositoryPort

class SubmitReview:
    """
    Use-case: submit a user review, given an IMDb ID.
    """

    def __init__(self, review_repo: ReviewRepositoryPort):
        self.review_repo = review_repo

    def execute(self, imdb_id: str, user_opinion: str, user_rating: int) -> None:
        # value object validation happens in the Review constructor
        review = Review(
            imdb_id=ImdbId(imdb_id),
            user_opinion=OpinionText(user_opinion),
            user_rating=Rating(user_rating)
        )
        self.review_repo.save(review)
