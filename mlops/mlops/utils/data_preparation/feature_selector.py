from typing import List, Optional

import pandas as pd

def select_features(df: pd.DataFrame, features: Optional[List[str]] = None) -> pd.DataFrame:
    return df[features]
