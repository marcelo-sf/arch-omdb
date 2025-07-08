import pytest
from domain.model.MovieAggregate import MovieAggregate
from domain.model.Review import Review
from domain.model.value.ImdbId import ImdbId
from domain.model.value.OpinionText import OpinionText
from domain.model.value.Rating import Rating

@pytest.fixture
def sample_aggregate():
    return MovieAggregate(
        imdb_id=ImdbId("tt123"),
        title="Title",
        year=2020,
        genre="Genre",
        director="Dir",
        actors=["A1", "A2"],
        imdb_rating="8.0",
        plot="Plot"
    )

def test_attach_no_reviews(sample_aggregate):
    assert sample_aggregate.reviews == []
    sample_aggregate.attach_reviews([])
    assert sample_aggregate.reviews == []

def test_attach_reviews(sample_aggregate):
    r1 = Review(ImdbId("tt123"), OpinionText("Good"), Rating(5))
    r2 = Review(ImdbId("tt123"), OpinionText("Bad"), Rating(3))
    sample_aggregate.attach_reviews([r1, r2])
    assert sample_aggregate.reviews == [r1, r2]

def test_attach_review_wrong_imdb(sample_aggregate):
    r = Review(ImdbId("tt999"), OpinionText("X"), Rating(4))
    with pytest.raises(ValueError):
        sample_aggregate.attach_reviews([r])

