from domain.model.Review import Review
from domain.model.value.ImdbId import ImdbId
from domain.model.value.OpinionText import OpinionText
from domain.model.value.Rating import Rating

def test_review_properties():
    rev = Review(imdb_id=ImdbId("tt000"), user_opinion=OpinionText("Op"), user_rating=Rating(7))
    assert rev.imdb_id == ImdbId("tt000")
    assert rev.user_opinion.value == "Op"
    assert rev.user_rating.value == 7

