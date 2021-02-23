from behave import *
from hamcrest import assert_that, is_


@when('checking the DPB1 alleles')
def step_impl(context):
    context.dpb1 = context.subjects['donor'].dpb1.potential_SLGs[0]

@then('the alleles are found to be "{dpb1}"')
def step_impl(context, dpb1):
    assert_that(context.dpb1.name, is_(dpb1))