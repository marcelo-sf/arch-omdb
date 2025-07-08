from behave import given, when, then
import requests

@given('the API gateway is running on port 80')
def step_api_running(context):
    # could poll /health here, but assume up
    pass

@when('I POST to "{path}" with body')
def step_post_with_body(context, path):
    url = f"{context.api_base}{path}"
    headers = {"Content-Type": "application/json"}
    context.response = requests.post(url, data=context.text, headers=headers)

@then("the response status code should be {code:d}")
def step_response_code(context, code):
    assert context.response.status_code == code, (
        f"Expected {code}, got {context.response.status_code}"
    )

@then('the response JSON should contain "{key}": "{value}"')
def step_response_json_contains(context, key, value):
    body = context.response.json()
    assert body.get(key) == value, (
        f'Expected JSON["{key}"] == "{value}", got {body}'
    )

