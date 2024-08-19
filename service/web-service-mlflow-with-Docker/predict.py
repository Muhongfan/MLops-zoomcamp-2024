import pickle
import os 
import pandas as pd
import json
from flask import Flask, request, jsonify
import mlflow

import boto3
from botocore.exceptions import NoCredentialsError

# Set the AWS profile environment variable
aws_profile = os.environ.get("AWS_PROFILE", "default")
RUN_ID = os.environ.get("RUN_ID", "default")
EXP_ID = os.environ.get("EXP_ID", "default")

os.environ["AWS_PROFILE"] = aws_profile

# Initialize a session using Amazon S3
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

logged_model = f's3://mlflow-artifacts-evs/{EXP_ID}/{RUN_ID}/artifacts/models'
model = mlflow.pyfunc.load_model(model_uri = logged_model, dst_path='./downloads/')

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