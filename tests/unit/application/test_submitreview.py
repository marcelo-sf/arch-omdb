from application.usecase.SubmitReview import SubmitReview
from domain.model.Review import Review
from domain.model.value.ImdbId import ImdbId
from domain.model.value.OpinionText import OpinionText
from domain.model.value.Rating import Rating

class FakeRepo:
    def __init__(self): self.saved = []
    def save(self, review: Review): self.saved.append(review)
    def find_by_imdb(self, imdb): return []

def test_submit_review_calls_save():
    repo = FakeRepo()
    uc = SubmitReview(repo)
    uc.execute(imdb_id="tt001", user_opinion="OK", user_rating=5)
    assert len(repo.saved) == 1
    saved = repo.saved[0]
    assert saved.imdb_id == ImdbId("tt001")
    assert saved.user_opinion == OpinionText("OK")
    assert saved.user_rating == Rating(5)

