import requests

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

url = 'http://localhost:1234/2015-03-31/functions/function/invocations'

# Assuming `event` is defined and contains the correct data
response = requests.post(url, json=event)

# Check the response status code
if response.status_code == 200:
    try:
        # Attempt to parse the JSON response
        data = response.json()
        print("JSON response:", data)
    except ValueError as json_error:
        # Handle JSON parsing error
        print("JSONDecodeError:", json_error)
        print("Response text:", response.text)  # Output the raw response for inspection
else:
    # Handle non-200 status codes
    print(f"Error: Received status code {response.status_code}")
    print("Response text:", response.text)  # Print the response content for debugging
    print("Response headers:", response.headers)  # Print response headers