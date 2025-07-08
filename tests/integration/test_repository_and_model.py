import pytest
from adapters.outgoing.persistence.sql_review_repo import SqlReviewRepo
from adapters.outgoing.persistence.models import Base
from domain.model.value.ImdbId import ImdbId
from domain.model.value.OpinionText import OpinionText
from domain.model.value.Rating import Rating
from domain.model.Review import Review as DomainReview
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def repo():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    orm_session_maker = sessionmaker(bind=engine)
    return SqlReviewRepo(orm_session_maker())

def test_save_and_query(repo):
    dr = DomainReview(ImdbId("tt10"), OpinionText("Good"), Rating(9))
    repo.save(dr)
    out = repo.find_by_imdb("tt10")
    assert len(out) == 1
    assert out[0].user_opinion.value == "Good"

