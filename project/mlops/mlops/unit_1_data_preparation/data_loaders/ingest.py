from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
import os
import numpy as np
import pandas as pd

from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_s3_bucket(*args, **kwargs):
    """
    Template for loading data from a S3 bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: /design/data-loading#s3
    """

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    print(ConfigFileLoader(config_path, config_profile))

    bucket_name = 'mlflow-artifacts-evs'
    object_key = 'data/energy_forecast.csv'
 
    data_file = S3.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )
    return data_file                                                                              

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """

    assert output is not None, 'The output is undefined'