Feature: Submit a movie review
  As a movie fan
  I want to submit my personal opinion and rating
  So that the system will store it for later viewing

  Background:
    Given the API gateway is running on port 80

  Scenario: successfully submit a valid review
    When I POST to "/create-movie:90" with body
      """
      {
        "imdb_id": "tt1375666",
        "user_opinion": "Stunning visuals!",
        "user_rating": 9
      }
      """
    Then the response status code should be 201
    And the response JSON should contain "status": "review saved"

  Scenario Outline: validation errors when submitting review
    When I POST to "/create-movie:90" with body:
      """
      {
        "imdb_id": "<imdb_id>",
        "user_opinion": "<opinion>",
        "user_rating": <rating>
      }
      """
    Then the response status code should be 4<error_code>

    Examples:
      | imdb_id     | opinion | rating | error_code |
      | wrong       | Bad     | 5      | 22         |
      | tt1234567   |         | 5      | 22         |
      | tt1234567   | Okay    | 11     | 22         |

