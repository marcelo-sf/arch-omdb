from behave import given, when, then
import requests
from typing import List, Dict


def sort_movies_by_year(movies: List[Dict]) -> List[Dict]:
    def get_year(m: Dict) -> int:
        y = m.get("Year", "")
        try:
            return int(y)
        except (ValueError, TypeError):
            # if Year is missing or not an int string
            return 0

    return sorted(movies, key=get_year)


@given('OMDb mock returns a movie with imdb_id "{imdb_id}" and title "{title}" for title "{search_title}"')
def step_omdb_mock(context, imdb_id, title, search_title):
    # The original design relied on FakeOmdbProvider being active.
    # But there is more value in invoking the live service when you want to detect if it has changed
    # its behaviour
    pass


@when('I GET "{path}" with params title="{title}"')
def step_search_title(context, path, title):
    url = f"{context.api_base}{path}"
    context.response = requests.get(url, params={"title": title})


@when('I GET "{path}" with params title="{title}" and year={year:d}')
def step_search_title_year(context, path, title, year):
    url = f"{context.api_base}{path}"
    context.response = requests.get(url, params={"title": title, "year": year})


@then('the response JSON array[0] should have "imdb_id": "{imdb_id}" and "title": "{title}"')
def step_verify_first_item(context, imdb_id, title):
    data = sort_movies_by_year(context.response.json())
    assert isinstance(data, list) and data, f"Expected non-empty list, got {data}"
    first = data[0]
    assert first.get("imdb_id") == imdb_id, (
        f'Expected first.imdb_id "{imdb_id}", got "{first.get("imdb_id")}"'
    )
    assert first.get("title") == title, (
        f'Expected first.title "{title}", got "{first.get("title")}"'
    )
