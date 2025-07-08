from application.usecase.SubmitReview import SubmitReview
from application.usecase.GetMovieDetails import GetMovieDetails
from application.usecase.SearchMovies import SearchMovies
from domain.port.provider.OmdbProviderPort import OmdbProviderPort
from domain.port.repository.ReviewRepositoryPort import ReviewRepositoryPort


class FakeOmdb(OmdbProviderPort):
    def fetch_by_id(self, imdb_id):
        return {
            "imdb_id": imdb_id,
            "title": "Blade Runner",
            "year": 1982,
            "genre": "Action, Drama, Sci-Fi",
            "director": "Ridley Scott",
            "actors": ["Harrison Ford, Rutger Hauer, Sean Young"],
            "imdb_rating": "8.1",
            "plot": "A blade runner must pursue and terminate four replicants who stole a ship in space and have returned to Earth to find their creator."
        }

    def search(self, title, year):
        return [{
            "imdb_id": "tt30",
            "title": "Blade Runner",
            "year": 1982,
            "genre": "Action, Drama, Sci-Fi",
            "director": "Ridley Scott",
            "actors": ["Harrison Ford, Rutger Hauer, Sean Young"],
            "imdb_rating": "8.1",
            "plot": "A blade runner must pursue and terminate four replicants who stole a ship in space and have returned to Earth to find their creator."
        }]


class FakeRepo(ReviewRepositoryPort):
    def __init__(self): self.data = []

    def save(self, review): self.data.append(review)

    def find_by_imdb(self, imdb_id): return self.data


from adapters.outgoing.omdb.omdb_acl_translator import OmdbACLTranslator

def test_end_to_end_flow():
    translator = OmdbACLTranslator()
    translator.register_handlers()

    repo = FakeRepo()
    submit = SubmitReview(repo)
    submit.execute("tt30", "OK", 5)
    
    get = GetMovieDetails(repo, FakeOmdb(), translator.translate_omdb_to_domain_type)
    details = get.execute(imdb_id="tt30")
    assert details.title == "Blade Runner"
    
    search = SearchMovies(repo, translator.translate_omdb_to_domain_type, {
        "title_only": FakeOmdb(),
        "title_year": FakeOmdb()
    })
    results = search.execute(title="Blade Runner", year=None)
    assert isinstance(results, list)