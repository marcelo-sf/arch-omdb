import os
import sys
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root)
sys.path.insert(0, os.path.join(root, "src"))

from adapters.incoming.fastapi.controllers import app, get_db_session as ctrl_get_db
from adapters.outgoing.persistence.models import Base
import config.container as container
from domain.port.provider.OmdbProviderPort import OmdbProviderPort

# Use a *single* in-memory SQLite DB shared by *all* connections
TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)
TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base.metadata.create_all(bind=engine)


def get_test_db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def override_dependencies() -> Generator[None, None, None]:
    app.dependency_overrides.clear()

    app.dependency_overrides[container.get_db_session] = get_test_db
    app.dependency_overrides[ctrl_get_db] = get_test_db

    class FakeOmdbProvider(OmdbProviderPort):
        def fetch_by_id(self, imdb_id: str) -> dict:
            return {
                "imdb_id": imdb_id,
                "title": "Fake Movie",
                "year": 2000,
                "genre": "Drama",
                "director": "Someone",
                "actors": ["Actor1", "Actor2"],
                "imdb_rating": "7.0",
                "plot": "A fake plot"
            }

        def search(self, title: str, year: int | None) -> list[dict]:
            return [self.fetch_by_id("tt2018")]

    app.dependency_overrides[container.get_omdb_client] = lambda: FakeOmdbProvider()

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
