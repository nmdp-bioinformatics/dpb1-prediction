from behave import *
from hamcrest import assert_that, is_
from dpb1.allele import Allele, InvalidAlleleError

@given('the allele name is {allele_name}')
def step_impl(context, allele_name):
    context.allele_name = allele_name
    
@when('evaluating the allele')
def step_impl(context):
    try:
        context.allele = Allele(context.allele_name)
        if context.allele.fields[0]:
            context.fields = ', '.join([f for f in context.allele.fields])
            context.resolution = context.allele.resolution
        else:
            context.fields = 'NA'
            context.resolution = 'NA'
        context.valid_allele = "valid"
    except InvalidAlleleError:
        context.valid_allele = "invalid"
        context.fields = "invalid"        
        context.resolution = "invalid"

@then('the allele name is found to be {validity}')
def step_impl(context, validity):
    assert_that(context.valid_allele, is_(validity))

@then('the field list is found to be {field_list}')
def step_impl(context, field_list):
    assert_that(context.fields, is_(field_list))

@then('the level of resolution is found to be {res_level}')
def step_impl(context, res_level):
    assert_that(context.resolution, is_(res_level))