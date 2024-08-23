from mlops.utils.data_preparation.cleaning import clean
from mlops.utils.data_preparation.feature_engineering import combine_features
from mlops.utils.data_preparation.feature_selector import select_features
from mlops.utils.data_preparation.splitters import split_on_value


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    features = ['day_of_week',  'created_date', 'chargeTimeHrs', 'distance', 'stationId', 'locationId']
    target = ['kwhTotal']

    df = clean(data)
    print("Succeffully cleaned data.")

    # df = combine_features(df)
    # print("Succeffully create additional relevant features")

    # df = select_features(df, features)
    X = df[features]
    y = df[target]    # print(df[features].drop(['kwhTotal'], axis=1))

    test_size = 0.2
    random_state = 42
    df_train, df_val = split_on_value(
        X,
        y,
        test_size,
        random_state
    )

    return df, df_train, df_val 


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    # df, df_train, df_val  = output
    assert output is not None, 'The output is undefined'