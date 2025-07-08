from dataclasses import dataclass

@dataclass
class ReviewRequest:
    """
    Input DTO for submitting a review.
    """
    imdb_id: str
    user_opinion: str
    user_rating: int
