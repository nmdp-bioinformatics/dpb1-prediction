from behave import *
from hamcrest import assert_that, is_
import dpb1.frequencies
from dpb1.haplotype import Haplotype
from sigfig import round

@when('obtaining the possible DPB1 alleles and frequencies for that haplotype')
def step_impl(context):
    context.haplotype._set_possible_DPB1s(context.ref_haplotypes_obs)

@when('extracting the DPB1 alleles for each haplotype within that genotype')
def step_impl(context):
    context.genotype.extract_DPB1_alleles(context.pop_freqs)

@then('the possible DPB1 alleles for that haplotype are "{allele_names}"')
def step_impl(context, allele_names):
    assert_that(','.join([dpb1.name for dpb1 in context.haplotype.dpb1_alleles]),
                is_(allele_names))

@then('the frequencies of those DPB1 alleles for that haplotype are "{allele_freqs}"')
def step_impl(context, allele_freqs):
    assert_that(','.join([str(round(float(dpb1.frequency), 3)) for dpb1 in context.haplotype.dpb1_alleles]),
                is_(allele_freqs))
