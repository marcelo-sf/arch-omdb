from application.usecase.GetMovieDetails import GetMovieDetails
from domain.port.provider.OmdbProviderPort import OmdbProviderPort
from domain.port.repository.ReviewRepositoryPort import ReviewRepositoryPort
from domain.model.value.ImdbId import ImdbId
from domain.model.Review import Review
from domain.model.value.OpinionText import OpinionText
from domain.model.value.Rating import Rating
from application.dto.MovieDetailsResponse import MovieDetailsResponse
from adapters.outgoing.omdb.omdb_acl_translator import OmdbACLTranslator


class FakeProvider(OmdbProviderPort):
    def fetch_by_id(self, imdb_id):
        return {
            "imdb_id": imdb_id,
            "title": "T",
            "year": 2020,
            "genre": "G",
            "director": "D",
            "actors": ["A"],
            "imdb_rating": "9.0",
            "plot": "P"
        }

    def search(self, title, year):
        """
        Intentionally empty override, functionality is not needed for this test case.
        """
        pass


class FakeRepo(ReviewRepositoryPort):
    def find_by_imdb(self, imdb_id):
        return [Review(ImdbId(imdb_id), OpinionText("good"), Rating(8))]

    def save(self, review):
        """
        Intentionally empty override, functionality is not needed for this test case.
        """
        pass


def test_get_movie_details_returns_response():
    provider = FakeProvider()
    repo = FakeRepo()

    # Initialize the translator and register attribute handlers
    translator = OmdbACLTranslator()
    translator.register_handlers()

    # Pass the translator's translate_omdb_to_domain_type method as an argument
    uc = GetMovieDetails(repo, provider, translator.translate_omdb_to_domain_type)

    resp = uc.execute(imdb_id="tt002")
    assert isinstance(resp, MovieDetailsResponse)
    assert resp.imdb_id == "tt002"
    assert len(resp.reviews) == 1