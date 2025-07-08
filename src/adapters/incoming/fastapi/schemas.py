from pydantic import BaseModel, Field
from typing import Optional


class ReviewRequest(BaseModel):
    imdb_id: str = Field(..., regex=r"^tt\d+$")
    user_opinion: str = Field(..., min_length=1)
    user_rating: int = Field(..., ge=1, le=10)


class MovieSearchParams(BaseModel):
    title: str
    year: Optional[int] = Field(
        default=None,
        description="Filter by year; can be omitted or empty string",
    )
