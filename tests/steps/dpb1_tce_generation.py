from behave import *
from hamcrest import assert_that, is_
from dpb1.tce import TCE_SLUG, TCE_map

@given('these expected TCE SLUGs')
def step_impl(context):
    context.tce_exp = []
    for row in context.table:
        context.tce_exp.append(TCE_SLUG(row['TCE SLUG'],
                                        probability=float(row['Probability'])))

@when('generating the DPB1 SLUGs and TCE groups for the {subject_types}')
def step_impl(context, subject_types):
    tce_map = TCE_map()
    for subject_type in subject_types.split('/'):
        subject = context.subjects[subject_type]
        dpb1_slgs = subject.generate_dpb1_slugs()
        tce_slgs = subject.generate_tce_genotypes()
        context.slugs_obs = subject._filter_epsilon(dpb1_slgs)
        context.tce_obs = subject._filter_epsilon(tce_slgs)

@then('the expected and observed TCE groups are the same')
def step_impl(context):
    assert_that(str(context.tce_obs), is_(str(context.tce_exp)))