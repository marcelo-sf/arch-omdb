import pytest
from httpx import AsyncClient
from fastapi import status
from adapters.incoming.fastapi.controllers import app


@pytest.mark.asyncio
async def test_create_movie_success():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(
            "/create-movie:90",
            json={
                "imdb_id": "tt001",
                "user_opinion": "O",
                "user_rating": 5
            },
        )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_create_movie_validation_error():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(
            "/create-movie:90",
            json={
                "imdb_id": "wrong",
                "user_opinion": "",
                "user_rating": 15
            },
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
