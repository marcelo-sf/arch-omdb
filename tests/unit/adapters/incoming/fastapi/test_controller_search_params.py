import pytest
from adapters.incoming.fastapi.search_params_adapter import SearchParamsAdapter
from src.adapters.incoming.fastapi.schemas import MovieSearchParams

@pytest.mark.asyncio
async def test_search_params_adapter_both_sources_with_title_and_year(mocker):
    json = MovieSearchParams(title="Inception", year=2010)
    params = MovieSearchParams(title="Interstellar", year=2014)
    result = await SearchParamsAdapter.adapt(json, params)
    assert result == {"title": "Interstellar", "year": 2014}

@pytest.mark.asyncio
async def test_search_params_adapter_only_json_source(mocker):
    json = MovieSearchParams(title="Inception", year=2010)
    params = MovieSearchParams(title="", year=None)
    result = await SearchParamsAdapter.adapt(json, params)
    assert result == {"title": "Inception", "year": 2010}

@pytest.mark.asyncio
async def test_search_params_adapter_only_query_params(mocker):
    json = MovieSearchParams(title="", year=None)
    params = MovieSearchParams(title="Interstellar", year=2014)
    result = await SearchParamsAdapter.adapt(json, params)
    assert result == {"title": "Interstellar", "year": 2014}

@pytest.mark.asyncio
async def test_search_params_adapter_combined_sources_preference(mocker):
    json = MovieSearchParams(title="Inception", year=None)
    params = MovieSearchParams(title="Interstellar", year=2014)
    result = await SearchParamsAdapter.adapt(json, params)
    assert result == {"title": "Interstellar", "year": 2014}

@pytest.mark.asyncio
async def test_search_params_adapter_empty_sources(mocker):
    json = MovieSearchParams(title="", year=None)
    params = MovieSearchParams(title="", year=None)
    result = await SearchParamsAdapter.adapt(json, params)
    assert result == {"title": "", "year": None}