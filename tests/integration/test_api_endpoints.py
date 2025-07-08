def test_full_api(client):
    new_review = {
        "user_opinion": "Nice",
        "user_rating": 6
    }

    new_review_request = new_review | {
        "imdb_id": "tt40"
    }

    r = client.post("/create-movie:90", json=new_review_request)
    assert r.status_code == 201
    movie_data = r.json()  # Parse the JSON response

    # Ensure required fields are present in the response
    assert "reviews" in movie_data, "The 'reviews' key is missing in the response."
    assert isinstance(movie_data["reviews"], list), "The 'reviews' field must be a list."
    assert any(review == new_review for review in movie_data["reviews"]), (
        "The new review was not found in the reviews list."
    )

    r3 = client.get("/search-movie:90", params={"title": "Ghost Busters", "year": ""})
    assert r3.status_code == 422

    r4 = client.get("/search-movie:90", params={"title": "Chariots of Fire"})
    assert r4.status_code == 200
    assert isinstance(r4.json(), list)

    r5 = client.get("/search-movie:90", params={"title": "Blade Runner", "year": 1982})
    assert r5.status_code == 200
    assert isinstance(r5.json(), list)

    # Add new tests for JSON payloads (using GET)
    # Test search-movie with invalid JSON payload (missing required fields or invalid values)
    r6 = client.request("GET", "/search-movie:90", json={"title": "The Blob", "year": ""})
    assert r6.status_code == 422

    # Test search-movie with valid JSON payload containing only "title"
    r7 = client.request("GET", "/search-movie:90", json={"title": "The Matrix"})
    assert r7.status_code == 200
    assert isinstance(r7.json(), list)

    # Test search-movie with valid JSON payload containing "title" and "year"
    r8 = client.request("GET", "/search-movie:90", json={"title": "Blade Runner", "year": 1982})
    assert r8.status_code == 200
    assert isinstance(r8.json(), list)

    # Test search-movie with a completely empty JSON payload
    r9 = client.request("GET", "/search-movie:90", json={})
    assert r9.status_code == 422

    # Test search-movie with unrelated or invalid JSON fields
    r10 = client.request("GET", "/search-movie:90", json={"invalid_field": "value"})
    assert r10.status_code == 422

    # Test search-movie with both query parameters and JSON payload
    # Ensures the adapter merges or overrides params correctly
    r11 = client.request(
        "GET",
        "/search-movie:90",
        params={"title": "Query Title", "year": "2000"},
        json={"title": "JSON Title", "year": 1982}
    )
    assert r11.status_code == 200
