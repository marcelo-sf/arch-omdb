import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.outgoing.factory import AdapterFactory
from adapters.outgoing.omdb.concrete_client import OmdbClient
from adapters.outgoing.omdb.mock_client import MockOmdbClient
from adapters.outgoing.persistence.sql_review_repo import SqlReviewRepo
from adapters.outgoing.omdb.omdb_acl_translator import OmdbACLTranslator

def test_create_omdb_client_default():
    client = AdapterFactory.create_omdb_client(api_key="test-key", use_mock=False)
    assert isinstance(client, OmdbClient)
    assert hasattr(client, "_translator")
    assert isinstance(client._translator, OmdbACLTranslator)


def test_create_omdb_client_mock():
    client = AdapterFactory.create_omdb_client(api_key="test-key", use_mock=True)
    assert isinstance(client, MockOmdbClient)

@pytest.fixture
def db_session():
    # Set up an in-memory SQLite session for testing
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    orm_session_maker = sessionmaker(bind=engine)
    orm_session_instance = orm_session_maker()
    yield orm_session_instance
    orm_session_instance.close()

def test_create_review_repository(db_session):
    repo = AdapterFactory.create_review_repository(db_session)
    assert isinstance(repo, SqlReviewRepo)

def create_omdb_translator():
    translator = OmdbACLTranslator()
    translator.register_handlers()
    return translator