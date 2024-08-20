from typing import Dict, List, Union

from pandas import DataFrame


def combine_features(df: Union[List[Dict], DataFrame]) -> Union[List[Dict], DataFrame]:
    if isinstance(df, DataFrame):
        df['Sta_Loc'] = df['stationId'].astype(str) + '_' + df['locationId'].astype(str)

    return df
