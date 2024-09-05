import json
import os 
import boto3
import pickle
import mlflow
import base64

TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

aws_profile = os.environ.get("AWS_PROFILE", "default")
print("aws_profile",aws_profile)
RUN_ID = os.environ.get("RUN_ID")
EXP_ID = os.environ.get("EXP_ID")
print("RUN_ID",RUN_ID)

os.environ["AWS_PROFILE"] = aws_profile

session = boto3.Session(profile_name=aws_profile)
# Retrieve the credentials
credentials = session.get_credentials()
# Set the credentials as environment variables
if credentials:
    os.environ["AWS_ACCESS_KEY_ID"] = credentials.access_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = credentials.secret_key
    
    # Set the session token if available
    if credentials.token:
        os.environ["AWS_SESSION_TOKEN"] = credentials.token
    
    # Set the default region if available
    if session.region_name:
        os.environ["AWS_DEFAULT_REGION"] = session.region_name

    print("Credentials are set as environment variables")
else:
    print("Credentials not available")

kinesis_client = boto3.client('kinesis')
PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME','default')

# def download_s3_folder(bucket_name, s3_folder, local_dir):
#     s3 = boto3.client('s3')
#     paginator = s3.get_paginator('list_objects_v2')
#     for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_folder):
#         for obj in page.get('Contents', []):
#             key = obj['Key']
#             # Create local file path
#             local_file_path = os.path.join(local_dir, os.path.relpath(key, s3_folder))
#             # Ensure the local directory exists
#             os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
#             # Download the file
#             s3.download_file(bucket_name, key, local_file_path)
#             print(f'Downloaded {key} to {local_file_path}')

# # Example function call
# download_s3_folder('mlflow-artifacts-evs', '4/ccb1e1f2811a426396410a62e6c81da5/artifacts/models', 'downloads')

# ENV RUN_ID=ccb1e1f2811a426396410a62e6c81da5
# ENV EXP_ID=4
logged_model = f's3://mlflow-artifacts-evs/{EXP_ID}/{RUN_ID}/artifacts/models'
model = mlflow.pyfunc.load_model(model_uri = logged_model, dst_path='./downloads/')
print("Finish loading the model!")

# # Fetch model dependencies
# dependencies = mlflow.pyfunc.get_model_dependencies(logged_model)

# # Save the dependencies to a file
# with open("model_dependencies.yaml", "w") as f:
#     f.write(dependencies)

def prepare_features(energy):
    features = {}
    columns = ['day_of_week', 'month', 'day', 'year', 'created_date', 'chargeTimeHrs', 'distance', 'Sta_Loc', 'stationId', 'locationId']
    for column in columns:
        features[column] = energy[column]  # Ensure `column` is not a list
    return features


def predict_energy(features):
    preds = model.predict(features)
    # preds = 223

    return preds

def lambda_handler(event):

    predictions_events = []
    # for record in event['Records']:
    #     encoded_data = record['kinesis']['data']
    #     decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    #     energy_event = json.loads(decoded_data)
    
    # for record in event['energy']:
    #     print(record)
    #     encoded_data = record['kinesis']['data']
    #     decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    #     ride_event = json.loads(decoded_data)

    #     ride = ride_event['ride']
    #     ride_id = ride_event['ride_id']

    #     features = prepare_features(ride)
    #     prediction = predict(features)

    #     prediction_event = {
    #         'model': 'ride_duration_prediction_model',
    #         'version': '123',
    #         'prediction': {
    #             'ride_duration': prediction,
    #             'ride_id': ride_id
    #         }
    #     }
    #     # print(json.dumps(prediction_event))

    
    
    if 'energy' not in event:
            return {
                "statusCode": 400,
                "body": "Error: 'energy' key is missing from the event data."
            }

    energy_input = event['energy']
    energy_real_time = event['energy']['target']
    energy_id = event['energy_id']
    
    features = prepare_features(energy_input)
    pred = predict_energy(features)
    prediction = {
         'kwhTotal': pred,
         'energy_real_time':energy_real_time,

    }
    print(prediction, "is prediction")
    print("Finish predicting")
    prediction_event = {
            'model': 'energy_consumption_prediction_model',
            'version': '111',
            'energy_session_id':energy_id,
            'prediction': {
                'energy_duration': prediction,
            }
        }

    if not TEST_RUN:
        kinesis_client.put_record(
        StreamName=PREDICTIONS_STREAM_NAME,
        Data=json.dumps(prediction_event),
        PartitionKey=str(332)
    )

    predictions_events.append(prediction_event) 
    print(predictions_events)

    return {

        'prediction': predictions_events

    }

event = {
    "energy": {
        "day_of_week": 2,
        "month": 9,
        "day": 9,
        "year": 2015,
        "created_date": "2015-09-09",
        "chargeTimeHrs": 2.923611111,
        "distance": 32.8745456,
        "Sta_Loc": "582873_461655",
        "stationId": "582873",
        "locationId": "461655",
        "target": 6.76,
        
    },
    "energy_id": str(112233445)
    }

print(lambda_handler(event))
