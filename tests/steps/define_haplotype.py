from behave import *
from hamcrest import assert_that, is_
from dpb1.haplotype import Haplotype

@given('the haplotype name as {haplotype_name}')
def step_impl(context, haplotype_name):
    context.haplotype_name = haplotype_name
    
@when('evaluating the validity of the haplotype name')
def step_impl(context):
    try:
        context.haplotype = Haplotype(context.haplotype_name)
        context.valid_haplotype = "valid"
    except:
        context.valid_haplotype = "invalid"

@then('the haplotype name is found to be {validity}')
def step_impl(context, validity):
    assert_that(context.valid_haplotype, is_(validity))


@given('the haplotype as "{haplotype_name}"')
def step_impl(context, haplotype_name):
    context.haplotype = Haplotype(name=haplotype_name)

@when('selecting specific allele names')
def step_impl(context):
    context.alleles = context.haplotype.alleles

@then('the allele {locus} is found to be {allele_name}')
def step_impl(context, locus, allele_name):
    assert_that(context.alleles[locus], is_(allele_name))