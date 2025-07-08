from typing import Generator, Dict
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from adapters.outgoing.omdb.search_strategies import TitleOnlyStrategy, TitleYearStrategy
from application.usecase.GetMovieDetails import GetMovieDetails
from application.usecase.SearchMovies import SearchMovies
from application.usecase.SubmitReview import SubmitReview
from config.settings import Settings
from adapters.outgoing.persistence.sql_review_repo import SqlReviewRepo
from domain.port.repository.ReviewRepositoryPort import ReviewRepositoryPort
from adapters.outgoing.omdb.concrete_client import OmdbClient
from domain.port.provider.OmdbProviderPort import OmdbProviderPort
from adapters.outgoing.omdb.omdb_acl_translator import OmdbACLTranslator

settings = Settings()

engine = create_engine(
    settings.database_url,
    echo=False,  # turn on if you need SQL logging
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db_session() -> Generator[Session, None, None]:
    """
    Yields a SQLAlchemy Session, closing it once the request is done.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_review_repo(
        session: Session = Depends(get_db_session)
) -> ReviewRepositoryPort:
    return SqlReviewRepo(session)


def get_omdb_client() -> OmdbProviderPort:
    return OmdbClient(api_key=settings.omdb_api_key)


def get_translator_method():
    translator = OmdbACLTranslator()
    translator.register_handlers()
    return translator.translate_omdb_to_domain_type


def get_search_strategies(
        omdb_client: OmdbProviderPort = Depends(get_omdb_client)
) -> Dict[str, object]:
    return {
        "title_only": TitleOnlyStrategy(omdb_client),
        "title_year": TitleYearStrategy(omdb_client),
    }


def get_submit_review_uc(
        repo: ReviewRepositoryPort = Depends(get_review_repo)
) -> SubmitReview:
    return SubmitReview(repo)


def get_movie_details_uc(
        repo: ReviewRepositoryPort = Depends(get_review_repo),
        omdb_client: OmdbProviderPort = Depends(get_omdb_client),
        translator_method=Depends(get_translator_method),
) -> GetMovieDetails:
    return GetMovieDetails(
        review_repo=repo,
        omdb_provider=omdb_client,
        translator=translator_method,
    )


def get_search_movies_uc(
        repo: ReviewRepositoryPort = Depends(get_review_repo),
        strategies: dict = Depends(get_search_strategies),
        translator_method=Depends(get_translator_method),
) -> SearchMovies:
    return SearchMovies(
        review_repo=repo,
        translator=translator_method,
        strategies=strategies
    )
