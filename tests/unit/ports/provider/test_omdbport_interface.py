from domain.port.provider.OmdbProviderPort import OmdbProviderPort

def test_interface_methods_exist():
    assert callable(getattr(OmdbProviderPort, "fetch_by_id", None))
    assert callable(getattr(OmdbProviderPort, "search", None))

