import pickle
import os 
import pandas as pd
import json
from flask import Flask, request, jsonify

# Set up the service on Flask
# file_path = os.path.join(os.getcwd(), 'models','xgboost_time_series_energy.bin')
# if not os.path.exists(file_path):
#     print(f"Model not found: {file_path}")

# Load the model
# with open(file_path, 'rb') as f_in:

with open('./xgboost_time_series_energy.bin', 'rb') as f_in:
    (dv,model) = pickle.load(f_in)

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
    X = dv.transform(features)
    preds = model.predict(X)
    return preds

app = Flask('energy-prediction')

@app.route('/predict', methods = ['POST'])
def predict_endpoint():
    energy = request.get_json()
    features = prepare_features(energy)
    pred = predict_energy(features)
    prediction = {
         'kwhTotal': pred
    }
    prediction['kwhTotal'] = prediction['kwhTotal'].tolist()

    # Convert the dictionary to JSON
    json_data = json.dumps(prediction)

    return jsonify(json_data)

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port = 9696)