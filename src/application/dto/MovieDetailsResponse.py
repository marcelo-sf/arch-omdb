from typing import List
from pydantic import BaseModel


class ReviewDto(BaseModel):
    user_opinion: str
    user_rating: int


class ActorDto(BaseModel):
    name: str


class MovieDetailsResponse(BaseModel):
    title: str
    year: int
    imdb_id: str
    genre: str
    director: str
    actors: List[ActorDto]
    imdb_rating: str
    plot: str
    reviews: List[ReviewDto]
