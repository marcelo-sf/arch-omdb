import pytest
from unittest.mock import patch, MagicMock
from adapters.outgoing.omdb.concrete_client import OmdbClient
from adapters.outgoing.omdb.omdb_acl_translator import OmdbACLTranslator


# Mock Translator for testing
@pytest.fixture
def mock_translator():
    translator = OmdbACLTranslator()
    translator.register_handlers()
    return translator


# Test parsing successful responses
def test_parse_expected_fields(monkeypatch, mock_translator):
    raw = {
        "imdbID": "tt1234567",
        "Title": "Test Movie",
        "Year": "2023",
        "Genre": "Drama",
        "Director": "Test Director",
        "Actors": "Actor1, Actor2",
        "imdbRating": "8.5",
        "Plot": "This is a test plot."
    }

    class MockResponse:
        status_code = 200

        def json(self):
            return raw

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())
    client = OmdbClient("test-api-key")
    client._translator = mock_translator  # Inject mock translator
    parsed_data = client.fetch_by_id("tt1234567")

    assert parsed_data["imdb_id"] == "tt1234567"
    assert parsed_data["actors"] == ["Actor1", "Actor2"]


# Test HTTP error handling
def test_handle_http_error(monkeypatch):
    class MockResponse:
        status_code = 404

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())
    client = OmdbClient("test-api-key")

    with pytest.raises(ConnectionError, match="OMDb HTTP 404"):
        client._get_with_retry({})


# Test API-specific errors
@patch("requests.get")
def test_handle_api_error(mock_get, mock_translator):
    mock_get.return_value = MagicMock(
        status_code=200, json=lambda: {"Error": "Invalid API key"}
    )
    client = OmdbClient("test-api-key")
    client._translator = mock_translator

    with pytest.raises(ValueError, match="OMDb API Error: Invalid API key"):
        client.fetch_by_id("invalid_id")


# Test parsing with missing fields
def test_parse_missing_fields(mock_translator):
    raw = {"imdbID": "tt", "Actors": "Actor1,Actor2"}  # Incomplete data
    client = OmdbClient("test-api-key")
    client._translator = mock_translator

    with pytest.raises(KeyError):
        client._parse(raw)


# Test search logic
@patch("adapters.outgoing.omdb.concrete_client.OmdbClient.fetch_by_id")
@patch("requests.get")
def test_search(mock_get, mock_fetch_by_id, mock_translator):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "Search": [{"imdbID": "tt1"}, {"imdbID": "tt2"}],
            "Response": "True",
        }
    )
    mock_fetch_by_id.side_effect = lambda imdb_id: {"imdb_id": imdb_id}
    client = OmdbClient("test-api-key")
    client._translator = mock_translator

    results = client.search("Test", year=2023)
    assert len(results) == 2
    assert results[0]["imdb_id"] == "tt1"
    assert results[1]["imdb_id"] == "tt2"


# Test search with no results
@patch("requests.get")
def test_search_no_results(mock_get, mock_translator):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"Response": "False"}
    )
    client = OmdbClient("test-api-key")
    client._translator = mock_translator

    results = client.search("Nonexistent Movie", year=2023)
    assert results == []
