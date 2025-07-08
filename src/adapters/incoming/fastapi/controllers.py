from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import JSONResponse
from adapters.incoming.fastapi.schemas import ReviewRequest, MovieSearchParams
from adapters.incoming.fastapi.search_params_adapter import SearchParamsAdapter, AdaptedSearchParams
from application.dto.MovieDetailsResponse import MovieDetailsResponse
from application.dto.MovieSearchResponse import MovieSearchResponse

from config.container import (
    get_db_session,
    get_submit_review_uc,
    get_search_movies_uc,
    get_movie_details_uc,
)

import logging
import traceback

from config.logging_setup import setup_logging

setup_logging()

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/health")
def health(db: Session = Depends(get_db_session)):
    """
    Health check endpoint verifies the DB connection.
    """
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Database unreachable")
    return JSONResponse(status_code=200, content={"status": "ok"})


@app.post("/create-movie:90", status_code=201)
def create_movie(
        req: ReviewRequest,
        uc=Depends(get_submit_review_uc),
        uc_details=Depends(get_movie_details_uc),
):
    try:
        uc.execute(
            imdb_id=req.imdb_id,
            user_opinion=req.user_opinion,
            user_rating=req.user_rating,
        )
        return uc_details.execute(imdb_id=req.imdb_id)
    except Exception as e:
        import traceback
        raise HTTPException(status_code=400, detail=str(e) + "\n" + traceback.format_exc())


@app.get("/search-movie:90", response_model=List[MovieSearchResponse])
async def search_movie(
        request: Request,
        # params: MovieSearchParams = Depends(),
        uc=Depends(get_search_movies_uc),
):
    try:
        try:
            json_payload = await request.json()
            try:
                json_payload = MovieSearchParams(title=json_payload.get("title"), year=json_payload.get("year"))
            except Exception as e:
                return JSONResponse(status_code=422, content={"detail": str(e)})
        except Exception:
            json_payload = None

        try:
            query_params = request.query_params
            params = MovieSearchParams(title=query_params.get('title'), year=query_params.get('year'))
            adapted_params = await SearchParamsAdapter.adapt(json_payload, params)
        except (ValidationError, TypeError) as e:
            adapted_params = AdaptedSearchParams(title=json_payload.title, year=json_payload.year)

        title = adapted_params.get("title")
        year = adapted_params.get("year")

        if not title:
            raise HTTPException(status_code=422, detail="`title` is required for movie search.")

        logger.info(f"Searching movies - Title: {title}, Year: {year if year else 'Not specified'}")

        results = uc.execute(title=title, year=year)

        logger.info(f"Found {len(results)} movies matching search criteria.")
        return JSONResponse(status_code=200, content=jsonable_encoder(results))

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e) + "\n" + traceback.format_exc())
