from behave import *
from hamcrest import assert_that, is_
from dpb1.haplotype import Haplotype
from dpb1.genotype import Genotype
from dpb1.imputation import Imputation

@given('these expected imputed genotypes')
def step_impl(context):
    genotypes = []
    for row in context.table:
        haplotype_1 = Haplotype(name = row['Haplotype 1'],
                                population = context.population,
                                frequency = float(row['Freq 1']))
        haplotype_2 = Haplotype(name = row['Haplotype 2'],
                                population = context.population,
                                frequency = float(row['Freq 2']))
        genotypes.append(Genotype([haplotype_1, haplotype_2]))
    context.imputation_exp = genotypes

@when('obtaining the imputed genotypes')
def step_impl(context):
    context.imputation_obs = context.subjects['donor']._impute()

@then('the expected versus obtained genotypes are found to be equal')
def step_impl(context):
    assert_that(str(context.imputation_obs), is_(str(context.imputation_exp)))