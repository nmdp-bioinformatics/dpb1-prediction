from behave import *
from hamcrest import assert_that, is_
from dpb1.subject import Subject
from dpb1.population import Population
from pyard import ARD
from dpb1.tce import TCE_map

@given('this set of typings')
def step_impl(context):
    context.glstring = []
    glstring = []
    for row in context.table:
        alleles = []
        for allele in row:
            if allele:
                alleles.append(allele)
        glstring.append("+".join(alleles))
    context.glstring = '^'.join(glstring)

@given("the subject's population code as '{population}'")
def step_impl(context, population):
    context.population = Population(population).code

@given("the resulting {subject_type} subject")
def step_impl(context, subject_type):
    tce_map = TCE_map()
    if not hasattr(context, 'subjects'):
        context.subjects = {}
    context.subjects[subject_type] = Subject(context.glstring,
                                             context.population,
                                             ref_freqs=context.ref_freqs,
                                             subject_type=subject_type,
                                             ard=context.ard,
                                             tce_map=tce_map)
    print(context.subjects[subject_type].imputation)

    # context.subjects = None

@given("these imputed phased multilocus unambiguous genotypes")     
def step_impl(context):
    print(context.table)

@when('focusing on the haplotype "{haplotype_name}"')
def step_impl(context, haplotype_name):
    for genotype in context.subjects['donor'].imputation.genotypes:
        for haplotype in genotype.haplotypes:
            if haplotype.name == haplotype_name:
                context.haplotype = haplotype
                pass

@when('focusing on the imputed genotype "{genotype_name}"')
def step_impl(context, genotype_name):
    for genotype in context.subjects['donor'].imputation.genotypes:
        if genotype.name == genotype_name:
            context.genotype = genotype
            pass