import requests
import json
import datetime

#   "kwhTotal": 6.76,

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

# Corrected data
energy = {
    "day_of_week": 2,
    "month": 9,
    "day": 9,
    "year": 2015,
    "created_date": "2015-09-09",  # Corrected date format
    "chargeTimeHrs": 2.923611111,
    "distance": 32.8745456,
    "Sta_Loc": "582873_461655",  # Corrected to string format
    "stationId":"582873",
    "locationId":"461655"
}

url = 'http://localhost:9696/predict'

try:
    # Send POST request with JSON data
    response = requests.post(url, json=energy)

    # Raise an HTTPError for bad responses
    response.raise_for_status()

    # Parse and print the JSON response
    data = response.json()
    print(data)
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as req_err:
    print(f"Request error occurred: {req_err}")
except ValueError as json_err:
    print(f"JSON decode error occurred: {json_err}")
