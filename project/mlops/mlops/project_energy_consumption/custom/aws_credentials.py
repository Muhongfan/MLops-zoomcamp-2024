import os
import boto3

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

os.environ["AWS_PROFILE"] = "mac2aws"
# Initialize a session using Amazon S3
session = boto3.Session(profile_name=os.environ["AWS_PROFILE"])
# Retrieve the credentials
credentials = session.get_credentials()
# # Get the access key, secret key, and session token
# access_key = credentials.access_key
# secret_key = credentials.secret_key
# session_token = credentials.token
# region = session.region_name

s3 = session.client('s3')


@custom
def transform_custom(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here

    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
