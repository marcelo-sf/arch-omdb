Feature: Search for movies
  As a user
  I want to search for movies by title and optionally by year
  So that I can discover movies with metadata and reviews

  Background:
    Given the API gateway is running on port 80
    And OMDb mock returns a movie with imdb_id "tt0133093" and title "The Matrix" for title "The Matrix"

  Scenario: find by title only
    When I GET "/search-movie:90" with params title="The Matrix"
    Then the response status code should be 200
    And the response JSON array[0] should have "imdb_id": "tt0133093" and "title": "The Matrix"

  Scenario: find by title and year
    When I GET "/search-movie:90" with params title="Lebowski" and year=1998
    Then the response status code should be 200
    And the response JSON array[0] should have "imdb_id": "tt0118715" and "title": "The Big Lebowski"

