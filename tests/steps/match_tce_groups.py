from behave import *
from hamcrest import assert_that, is_
from dpb1.match import Matches, MatchGrade
from dpb1.dpb1 import DPB1_SLUG
from dpb1.tce import TCE_SLUG
# from validation.dpb1_validator.observed import ObservedPair

@given('these TCE group pairs and expected match categories')
def step_impl(context):
    context.recip_tces = []
    context.donor_tces = []
    context.match_cats_exp = []
    for row in context.table:
        context.recip_tces.append(row['Recipient TCE'])
        context.donor_tces.append(row['Donor TCE'])
        context.match_cats_exp.append(row['Match Categories'])

@when('classifying their match categories')
def step_impl(context):
    context.match_cats_obs = []
    for i in range(len(context.recip_tces)):
        recip_tce = context.recip_tces[i]
        donor_tce = context.donor_tces[i]
        match_cat = MatchGrade([TCE_SLUG(recip_tce), TCE_SLUG(donor_tce)]).name
        # match_cat_ref = ObservedPair()._call_tce_match_grades(recip_tceg=recip_tce,
        #                                                       donor_tceg=donor_tce)
        # if match_cat != match_cat_ref:
        #     raise Exception("For recipient (%s) and donor (%s) TCEGs,"
        #                     " The calculated category (%s) does not equal"
        #                     " the referenced service (%s)"
        #                      % (recip_tce, donor_tce,
        #                         match_cat,
        #                         match_cat_ref))
        context.match_cats_obs.append(match_cat)

@then('their expected and classified categories are the same')
def step_impl(context):
    assert_that(context.match_cats_obs, is_(context.match_cats_exp))


@given('these expected match categories and probabilities')
def step_impl(context):
    context.matches_tce_exp = []
    for row in context.table:
        context.matches_tce_exp.append(MatchGrade([], name=row['Match category'],
                                       probability=float(row['Probability'])))

@when('obtaining the TCE match categories between the recipient and donor')
def step_impl(context):
    matches = Matches(context.subjects['recipient'], context.subjects['donor'])
    matches.get_tce_match_grades()
    context.matches_tce_obs = matches

@then('the expected and observed TCE match categories are the same')
def step_impl(context):
    assert_that(str(context.matches_tce_obs), is_(str(context.matches_tce_exp)))