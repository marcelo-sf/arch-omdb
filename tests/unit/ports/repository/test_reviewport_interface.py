from domain.port.repository.ReviewRepositoryPort import ReviewRepositoryPort

def test_interface_methods_exist():
    assert callable(getattr(ReviewRepositoryPort, "save", None))
    assert callable(getattr(ReviewRepositoryPort, "find_by_imdb", None))

