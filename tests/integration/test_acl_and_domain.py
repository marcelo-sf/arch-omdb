from adapters.outgoing.omdb.omdb_acl_translator import OmdbACLTranslator
from application.usecase.GetMovieDetails import GetMovieDetails
from application.usecase.SubmitReview import SubmitReview
from tests.integration.test_application_end_to_end import FakeRepo, FakeOmdb


def test_end_to_end_flow():
    translator = OmdbACLTranslator()
    translator.register_handlers()

    repo = FakeRepo()
    submit = SubmitReview(repo)
    submit.execute("tt30", "OK", 5)

    get = GetMovieDetails(repo, FakeOmdb(), translator.translate_omdb_to_domain_type)
    details = get.execute(imdb_id="tt30")
    assert details.title == "Blade Runner"