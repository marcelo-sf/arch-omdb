from typing import List
from pydantic import BaseModel


class ReviewDto(BaseModel):
    user_opinion: str
    user_rating: int


class MovieSearchResponse(BaseModel):
    title: str
    year: int
    imdb_id: str
    genre: str
    imdb_rating: str
    reviews: List[ReviewDto]
