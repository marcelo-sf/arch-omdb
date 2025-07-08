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

def test_save_and_find(repo):
    rev = DomainReview(ImdbId("tt003"), OpinionText("X"), Rating(6))
    repo.save(rev)
    out = repo.find_by_imdb("tt003")
    assert len(out) == 1
    assert out[0].user_rating.value == 6

