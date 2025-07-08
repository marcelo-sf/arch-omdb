from behave import given, when, then
import requests

@given('a movie review exists for "{imdb_id}" with opinion "{opinion}" and rating {rating:d}')
def step_create_review(context, imdb_id, opinion, rating):
    url = f"{context.api_base}/create-movie:90"
    payload = {
        "imdb_id": imdb_id,
        "user_opinion": opinion,
        "user_rating": rating
    }
    r = requests.post(url, json=payload)
    assert r.status_code == 201, f"Setup review failed: {r.text}"

@when('I GET "{path}" with query imdb_id="{imdb_id}"')
def step_get_movie(context, path, imdb_id):
    url = f"{context.api_base}{path}"
    context.response = requests.get(url, params={"imdb_id": imdb_id})

@then('the response JSON array "reviews" should contain an object with "user_opinion": "{opinion}" and "user_rating": {rating:d}')
def step_json_array_reviews_contains(context, opinion, rating):
    data = context.response.json()
    reviews = data.get("reviews", [])
    assert any(
        rev.get("user_opinion") == opinion and rev.get("user_rating") == rating
        for rev in reviews
    ), f"Did not find review {{opinion: {opinion}, rating: {rating}}} in {reviews}"

