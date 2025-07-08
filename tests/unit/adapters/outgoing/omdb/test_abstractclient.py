import pytest
from adapters.outgoing.omdb.abstract_client import AbstractOmdbClient
import requests

class DummyClient(AbstractOmdbClient):
    def _parse(self, raw): return raw

def test_handle_http_error(monkeypatch):
    class Resp: status_code = 500
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: Resp())
    client = DummyClient("k")
    with pytest.raises(ConnectionError):
        client.fetch_by_id("tt")

def test_handle_api_error(monkeypatch):
    class Resp:
        status_code = 200
        def json(self): return {"Error": "Bad"}
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: Resp())
    client = DummyClient("k")
    with pytest.raises(ValueError):
        client.fetch_by_id("tt")

