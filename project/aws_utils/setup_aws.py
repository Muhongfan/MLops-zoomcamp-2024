import boto3
import os
from botocore.exceptions import NoCredentialsError
from ruamel.yaml import YAML

os.environ["AWS_PROFILE"] = "mac2aws"

# Initialize a session using Amazon S3
session = boto3.Session(profile_name='mac2aws')

# Retrieve the credentials
credentials = session.get_credentials()

# Get the access key, secret key, and session token
access_key = credentials.access_key
secret_key = credentials.secret_key
session_token = credentials.token
region = session.region_name

# New data 
data = {

        'AWS_PROFILE': os.environ["AWS_PROFILE"],
        'AWS_ACCESS_KEY_ID': credentials.access_key,
        'AWS_SECRET_ACCESS_KEY': credentials.secret_key,
        'AWS_SESSION_TOKEN': credentials.token,
        'AWS_REGION': region
}

# Find the dir location
file_dir = os.getcwd()
new_dir_name = file_dir.replace('/utilis', '/')

# Initialize YAML object
yaml = YAML()
yaml.preserve_quotes = True  
yaml.indent(mapping=2, sequence=4, offset=2)  
yaml_file= os.path.join(new_dir_name, 'mlops/mlops/unit_1_data_preparation/', 'io_config.yaml')

# Load the existing YAML file
try:
    with open(yaml_file, 'r') as file:
        existing_data = yaml.load(file)
except FileNotFoundError:
    existing_data = {'version': '0.1.1', 'default': {}}

# # Ensure the 'default' section exists
if 'default' in existing_data:
    # existing_data['default'] = {}

    # Update the 'default' section with new data
    existing_data['default'].update(data)

# Save the updated data back to the YAML file
with open(yaml_file, 'w') as file:
    yaml.dump(existing_data, file)

print("Yaml file has been updated")


# Connect to s3
s3 = session.client('s3')
bucket_name = 'mlflow-artifacts-evs'

data_file_name = os.path.join(new_dir_name, 'data', 'station_data_dataverse.csv')
if not os.path.exists(data_file_name):
    print(f"File not found: {data_file_name}")

# The desired S3 object name (can be the same as data_file_name)
object_name = 'data/energy_forecast.csv'

try:
    # Upload the file
    s3.upload_file(data_file_name, bucket_name, object_name)
    print(f"Upload successful: {data_file_name} to s3://{bucket_name}/{object_name}")
except FileNotFoundError:
    print("The file was not found")
except NoCredentialsError:
    print("Credentials not available")




