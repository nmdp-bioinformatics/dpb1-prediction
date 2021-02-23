from behave import *
from hamcrest import assert_that, is_
from dpb1.haplotype import Haplotype

@given('these relevant reference haplotype frequencies for that population')
def step_impl(context):
    context.ref_freqs = context.hap_freqs.get_pop_freqs(context.population)
    pass

@given('these expected sorted reference frequencies for "{haplotype_name}"')
def step_impl(context, haplotype_name):
    context.ref_haplotypes_exp = []
    for row in context.table:
        context.ref_haplotypes_exp.append(Haplotype(name=row['Haplotype'],
                                 population=context.population,
                                 frequency=float(row['Freq'])))

@when('obtaining the sorted reference haplotype frequencies for that haplotype')
def step_impl(context):
    context.ref_haplotypes_obs = context.ref_freqs.get_possible_haplotypes(context.haplotype)

@then('the expected and obtained sorted reference haplotype frequencies are the same')
def step_impl(context):
    assert_that(str(context.ref_haplotypes_obs), is_(str(context.ref_haplotypes_exp)))