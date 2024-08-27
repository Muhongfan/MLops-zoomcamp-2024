from scipy.sparse import csr_matrix
from pandas import Series

from mlops.utils.data_preparation.encoders import vectorize_features
from mlops.utils.data_preparation.feature_selector import select_features

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    df, df_train, df_val = data
    target = kwargs.get('target', 'kwhTotal')

    # Drop 'kwhTotal' and pass the resulting DataFrame to vectorize_features
    X = df.drop(columns=['kwhTotal'])
    y: Series = df[target]

    X_train, X_val, dv = vectorize_features(
        df_train.drop(columns=['kwhTotal']),
        df_val.drop(columns=['kwhTotal'])
    )

    # Continue with the rest of your code
    y_train = df_train[target]
    y_val = df_val[target]
    print(df.shape,  X_train.shape, X_val.shape)

    return X, X_train, X_val, y, y_train, y_val, dv

@test
def test_dataset(
    X: csr_matrix,
    X_train: csr_matrix,
    X_val: csr_matrix,
    y: Series,
    y_train: Series,
    y_val: Series,
    *args,
) -> None:
    assert (
        X.shape[0] == 2331
    ), f'Entire dataset should have 2331 examples, but it has {X.shape[0]}'
    assert(
        X.shape[1] == 6
    ), f'Entire dataset should have 6 features, but it has {X.shape[1]}'
    assert(
        len(y.index) == X.shape[0]
    ), f'There are not the same number of y examples and X examples, there are {len(y.index)} y values and {X.shape[0]} X values'
@test
def test_training_set(
    X: csr_matrix,
    X_train: csr_matrix,
    X_val: csr_matrix,
    y: Series,
    y_train: Series,
    y_val: Series,
    *args,
) -> None:
    assert (
        X_train.shape[0] == 1864
    ), f'X_train should have 1864 examples, but it has {X_train.shape[0]}'
    assert(
        X_train.shape[1] == 332
    ), f'X_train should have 13 features, but it has {X_train.shape[1]}'
    assert(
        len(y_train.index) == X_train.shape[0]
    ), f'There are not the same number of y_train examples and X_train examples, there are {len(y_train.index)} y_train values and {X_train.shape[0]} X_train values'
@test
def test_validation_set(
    X: csr_matrix,
    X_train: csr_matrix,
    X_val: csr_matrix,
    y: Series,
    y_train: Series,
    y_val: Series,
    *args,
) -> None:
    assert (
        X_val.shape[0] == 467
    ), f'X_val should have 467 examples, but it has {X_val.shape[0]}'
    assert(
        X_val.shape[1] == 332
    ), f'X_val should have 13 features, but it has {X_val.shape[1]}'
    assert(
        len(y_val.index) == X_val.shape[0]
    ), f'There are not the same number of y_val examples and X_val examples, there are {len(y_val.index)} y_val values and {X_val.shape[0]} X_val values'

