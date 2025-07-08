from application.usecase.SearchMovies import SearchMovies
from domain.port.provider.OmdbProviderPort import OmdbProviderPort
from domain.port.repository.ReviewRepositoryPort import ReviewRepositoryPort
from adapters.outgoing.omdb.search_strategies import TitleOnlyStrategy, TitleYearStrategy
from adapters.outgoing.omdb.omdb_acl_translator import OmdbACLTranslator

class FakeRepo(ReviewRepositoryPort):
    def find_by_imdb(self, imdb_id):
        return []

    def save(self, review):
        """
        Intentionally empty override, functionality is not needed for this test case.
        """
        pass


class FakeTranslator:
    def to_domain(self, raw):
        class M: pass

        m = M()
        m.imdb_id = raw["imdb_id"]
        m.attach_reviews = lambda reviews: setattr(m, "reviews", reviews)
        return m


def test_search_title_only_strategy():
    raw = [{"imdb_id": "tt01"}]

    class FakeOmdb(OmdbProviderPort):
        def search(self, title, year):
            # Expect exactly these args
            assert title == "X"
            assert year is None
            return raw

        def fetch_by_id(self, imdb_id):
            """
            Mock implementation not used in this test
            """
            pass

    strat = TitleOnlyStrategy(FakeOmdb())
    assert strat.search("X", None) == raw


def test_search_year_strategy():
    raw = [{"imdb_id": "tt02"}]

    class FakeOmdb(OmdbProviderPort):
        def search(self, title, year):
            assert title == "Y"
            assert year == 2021
            return raw

        def fetch_by_id(self, imdb_id):
            """
            Mock implementation not used in this test
            """
            pass

    strat = TitleYearStrategy(FakeOmdb())
    assert strat.search("Y", 2021) == raw


def test_searchmovies_strategy_selection():
    translator = OmdbACLTranslator()
    translator.register_handlers()

    raw = [{"imdb_id": "tt03", "title": "Some Title", "year": 1983, "genre": "G", "director": "D", "actors": ["A"], "imdb_rating": "9.0", "plot": "P"}]

    class FakeOmdb(OmdbProviderPort):
        def search(self, title, year):
            assert title == "Some Title"
            assert year == 1983
            return raw

        def fetch_by_id(self, imdb_id):
            """
            Mock implementation not used in this test
            """
            pass

    strategies = {
        "title_only": TitleOnlyStrategy(FakeOmdb()),
        "title_year": TitleYearStrategy(FakeOmdb()),
    }
    uc = SearchMovies(FakeRepo(), translator.translate_omdb_to_domain_type, strategies)

    results = uc.execute(title="Some Title", year=1983)
    assert isinstance(results, list)
    assert results[0].title == "Some Title"