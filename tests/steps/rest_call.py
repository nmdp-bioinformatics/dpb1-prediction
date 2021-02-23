from behave import *
from hamcrest import assert_that, is_
import json

@given('an input payload as')
def step_impl(context):
    context.payload = json.loads(context.text)

@when("submitting the subject's information to and retrieving results from '{endpoint}'")
def step_impl(context, endpoint):
    results = context.client.post(endpoint, json=context.payload, follow_redirects=True)
    context.results = json.loads(results.data)

@then("the output is found to be")
def step_impl(context):
    assert_that(context.results, is_(json.loads(context.text)))