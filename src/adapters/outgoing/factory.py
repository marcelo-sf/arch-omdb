from sqlalchemy.orm import Session
from domain.port.provider.OmdbProviderPort import OmdbProviderPort
from domain.port.repository.ReviewRepositoryPort import ReviewRepositoryPort
from adapters.outgoing.omdb.concrete_client import OmdbClient
from adapters.outgoing.omdb.mock_client import MockOmdbClient
from adapters.outgoing.persistence.sql_review_repo import SqlReviewRepo


class AdapterFactory:
    """
    Central factory for all outgoing adapters.
    """

    @staticmethod
    def create_omdb_client(
        api_key: str,
        use_mock: bool = False
    ) -> OmdbProviderPort:
        """
        Instantiate the OMDb provider.

        :param api_key: your OMDb API key.
        :param use_mock: if True, returns a MockOmdbClient for tests.
        :return: an object implementing OmdbProviderPort.
        """
        if use_mock:
            return MockOmdbClient()
        return OmdbClient(api_key)

    @staticmethod
    def create_review_repository(
        db_session: Session
    ) -> ReviewRepositoryPort:
        """
        Instantiate the review repository backed by PostgreSQL.

        :param db_session: an active SQLAlchemy Session.
        :return: an object implementing ReviewRepositoryPort.
        """
        return SqlReviewRepo(db_session)
