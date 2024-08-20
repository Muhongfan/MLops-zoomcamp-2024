from typing import List, Tuple, Union
from sklearn.model_selection import train_test_split
import pandas as pd


def split_on_value(
    X: pd.DataFrame,
    y: pd.DataFrame,
    test_size: float,
    random_state: int,
):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Combine X_train and y_train to form df_train
    df_train = pd.concat([X_train, y_train], axis=1)

    # Combine X_test and y_test to form df_val
    df_val = pd.concat([X_test, y_test], axis=1)


    return df_train, df_val
