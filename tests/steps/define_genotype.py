from behave import *
from hamcrest import assert_that, is_
from dpb1.genotype import Genotype, InvalidGenotypeError

@given('the genotype name as {genotype_name}')
def step_impl(context, genotype_name):
    context.genotype_name = genotype_name
    
@when('evaluating the validity of the genotype name')
def step_impl(context):
    try:
        context.genotype = Genotype(context.genotype_name)
        context.valid_genotype = "valid"
    except:
        context.valid_genotype = "invalid"

@then('the genotype name is found to be {validity}')
def step_impl(context, validity):
    assert_that(context.valid_genotype, is_(validity))