from behave import *
from hamcrest import assert_that, is_
from dpb1.haplotype import Haplotype
from dpb1.dpb1 import DPB1_SLUG

@given('these expected SLUGs')
def step_impl(context):
    context.slugs_exp = []
    for row in context.table:
        freq = row["Probability"]
        context.slugs_exp.append(DPB1_SLUG(name=row["SLUG"],
                                           probability= None if freq == 'None' else float(freq)))

@when('generating all DPB1 SLUGs with a probability greater than 0.01 for the {subject_types}')
def step_impl(context, subject_types):
    for subject_type in subject_types.split('/'):
        subject = context.subjects[subject_type]
        subject.generate_dpb1_slugs()
        subject.filter_SLGs()
        context.slugs_obs = subject.SLUGs

@then('the expected and observed DPB1 SLUGs are found to be the same')
def step_impl(context):
    assert_that(str(context.slugs_obs), is_(str(context.slugs_exp)))