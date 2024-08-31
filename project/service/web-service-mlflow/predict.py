import pickle
import os 
import pandas as pd
import json
from flask import Flask, request, jsonify
import mlflow

import boto3
from botocore.exceptions import NoCredentialsError

# Set the AWS profile environment variable
os.environ["AWS_PROFILE"] = "mac2aws"

# Initialize a session using Amazon S3
session = boto3.Session(profile_name='mac2aws')

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

RUN_ID= '55703e594fdc4cf2a3958502b7c10b9e'
EXP_ID = 4
logged_model = f's3://mlflow-artifacts-evs/{EXP_ID}/{RUN_ID}/artifacts/models'
model = mlflow.pyfunc.load_model(model_uri = logged_model, dst_path='./downloads/')

# # Load model from MLFLOW tracking server
# TRACKING_SERVER_HOST = "ec2-3-14-112-137.us-east-2.compute.amazonaws.com" # fill in with the public DNS of the EC2 instance
# mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
# RUN_ID= '93171fded89c469ba246e1432521682c'
# mlflow.artifacts.download_artifacts(run_id = RUN_ID, artifact_path = 'xgboost_time_series_energy.bin', dst_path='./downloads/')

# # Load model from S3
# RUN_ID= '55703e594fdc4cf2a3958502b7c10b9e'
# artifacts = f's3://mlflow-artifacts-evs/4/{RUN_ID}/artifacts/xgboost_time_series_energy.bin'

# # Load the artifacts
# mlflow.artifacts.download_artifacts(artifact_uri = artifacts, dst_path='./downloads/')

# with open('./downloads/xgboost_time_series_energy.bin', 'rb') as f_in:
#     (dv, model) = pickle.load(f_in)

# Perpare the features
def prepare_features(energy):
    features = {}
    features["day_of_week"] = energy["day_of_week"]
    features["month"] = energy["month"]
    features["day"] = energy["day"]
    features["year"] = energy["year"]
    features["created_date"] = energy["created_date"]
    features["chargeTimeHrs"] = energy["chargeTimeHrs"]
    features["distance"] = energy["distance"]
    features["Sta_Loc"] = energy["Sta_Loc"]
    features["stationId"] = energy["stationId"]
    features["locationId"] = energy["locationId"]

    return features


def predict_energy(features):
    preds = model.predict(features)
    # X = dv.transform(features)
    # preds = model.predict(X)
    return preds

app = Flask('energy-prediction')

@app.route('/predict', methods = ['POST'])
def predict_endpoint():
    energy = request.get_json()
    features = prepare_features(energy)
    pred = predict_energy(features)
    prediction = {
         'kwhTotal': pred,
    }
    prediction['kwhTotal'] = prediction['kwhTotal'].tolist()

    # Convert the dictionary to JSON
    json_data = json.dumps(prediction)

    return jsonify(json_data)

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port = 9696)