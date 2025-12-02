from behave import *
from hamcrest import assert_that, is_
# from validation.dpb1_validator.predicted import Predicted, PredictedPair
import pandas as pd
from sigfig import round
import json

@given('a row (#{row_index}) in "{df_file_name}"')
def step_impl(context, row_index, df_file_name):
    context.df = pd.read_csv(df_file_name)
    context.row_index = int(row_index)

@when('generating the predicted permissive frequencies')
def step_impl(context):
    dpb1_predicted_pair = PredictedPair()
    rows = context.df.iloc[context.row_index:context.row_index+1]
    params = dpb1_predicted_pair.generate_params_matching(rows)
    print(json.dumps(params))
    results = dpb1_predicted_pair.call_tce_pred_match(params, url="http://localhost:5010")
    predicted_freq = dpb1_predicted_pair.get_perm_freq(results['data'][0])
    context.predicted_freq = (isinstance(predicted_freq, float) and 
                                str(round(predicted_freq, 3)) or predicted_freq)

@then('the expected {expected_freq} and predicted frequencies are the same')
def step_impl(context, expected_freq):
    assert_that(context.predicted_freq, is_(expected_freq))
