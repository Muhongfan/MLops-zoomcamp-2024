from typing import Dict, List, Tuple, Union

from sklearn.feature_extraction import DictVectorizer
from xgboost import Booster

from mlops.utils.data_preparation.feature_engineering import combine_features
from mlops.utils.models.xgboost import build_data

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

DEFAULT_INPUTS = [
            # "kwhTotal": 6.99,

            {
                "day_of_week": 0,
                   
                "month": 7,

                "day": 27,

                "year": 2015,

                "created_date":2015-07-27,

                "chargeTimeHrs": 2.720555556,

                "distance": 28.5290954,

                "Sta_Loc":874950_814002,

                },
                # "kwhTotal": 6.76,
                {
                "day_of_week": 2,
                   
                "month": 9,

                "day": 9,

                "year": 2015,

                "created_date":2015-09-09,

                "chargeTimeHrs": 2.923611111,

                "distance": 32.8745456,

                "Sta_Loc":369001_493904,

                },
]


@custom
def predict(
    model_settings: Dict[str, Tuple[Booster, DictVectorizer]],
    **kwargs,
) -> List[float]:
    inputs: List[Dict[str, Union[float, int]]] = kwargs.get('inputs', DEFAULT_INPUTS)
    inputs = combine_features(inputs)

    DOLocationID = kwargs.get('DOLocationID')
    PULocationID = kwargs.get('PULocationID')
    trip_distance = kwargs.get('trip_distance')

    if DOLocationID is not None or PULocationID is not None or trip_distance is not None:
        inputs = [
            {
                'DOLocationID': DOLocationID,
                'PULocationID': PULocationID,
                'trip_distance': trip_distance,
            },
        ]
    
    model, vectorizer = model_settings['xgboost']
    vectors = vectorizer.transform(inputs)

    predictions = model.predict(build_data(vectors))

    for idx, input_feature in enumerate(inputs):
        print(f'Prediction of duration using these features: {predictions[idx]}')
        for key, value in inputs[idx].items():
            print(f'\t{key}: {value}')

    return predictions.tolist()
