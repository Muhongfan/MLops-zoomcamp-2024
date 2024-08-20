import pandas as pd


    

def clean(
    df: pd.DataFrame,
    include_extreme_durations: bool = False,
) -> pd.DataFrame:
    df['created'] = pd.to_datetime(df['created'], errors='coerce')

    # Drop the rows if 'kwhTotal' is 0, and 'chargeTimeHrs' > 50
    df_non_zero = df.drop(df[df['kwhTotal'] == 0].index)
    df_non_zero = df_non_zero.drop(df_non_zero[df_non_zero['chargeTimeHrs'] > 50].index)

    # Clean the rows related with 'distance'
    df_non_zero["distance_missing"] = df_non_zero["distance"]
    # Category the 'distance'
    df_non_zero["distance_missing"] = False
    df_non_zero.loc[df_non_zero[df_non_zero['distance'].isnull()].index, "distance_missing"] = True
    df_non_zero['distance_missing'] = df_non_zero['distance_missing'].apply(lambda x: 1 if x else 0)

    # Group by userId and count occurrences for each condition
    missing_counts = df_non_zero[df_non_zero['distance_missing'] == 1]['userId'].value_counts()
    not_missing_counts = df_non_zero[df_non_zero['distance_missing'] == 0]['userId'].value_counts()

    # Check the users whose 'distance' are all missing 
    all_user_ids = missing_counts.index.union(not_missing_counts.index)
    missing_counts = missing_counts.reindex(all_user_ids, fill_value=0)
    not_missing_counts = not_missing_counts.reindex(all_user_ids, fill_value=0)

    # Calculate the difference
    difference = missing_counts - not_missing_counts

    # Find userIds where the difference matches the missing_counts
    result_user_ids = difference[difference == missing_counts].index

    # Filter the DataFrame
    df_filtered = df_non_zero[~df_non_zero['userId'].isin(result_user_ids)]

    # Replace where 'distance' with mean value where 'distance' is missing
    df_filtered.distance.fillna(df_filtered.distance.mean(), inplace=True)

    categorical = ['stationId', 'locationId']
    df_filtered[categorical] = df_filtered[categorical].astype(str)

    return df_filtered
