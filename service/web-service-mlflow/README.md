# Set up the web service with could & docker 

1. Create the folder "web-service". The tree of the folder is 
```
(base) (web-service-mlflow) amberm@Ambers-Air-2 web-service-mlflow % tree
.
├── Pipfile
├── Pipfile.lock
├── README.md
├── aws_credentials.py
├── data
│   ├── df_filtered.csv
│   └── station_data_dataverse.csv
├── downloads
│   └── models
│       ├── MLmodel
│       ├── conda.yaml
│       ├── model.pkl
│       ├── python_env.yaml
│       └── requirements.txt
├── energy_forecast.ipynb
├── mlflow.db
├── predict.py
└── test.py
```

2. Install `pipenv` for creating the virtual environment.
    
    `sudo -H pip install -U pipenv`

or activate the current virtual environment by `pipenv shell`.

3. Set up the pipeline of [model training](energy_forecast.ipynb) in jupyter notebook.

4. Set up aws

5. Load model 
    * Load artifacts from mlflow
    ```
    # Load model from MLFLOW tracking server
    TRACKING_SERVER_HOST = "ec2-3-14-112-137.us-east-2.compute.amazonaws.com" # fill in with the public DNS of the EC2 instance
    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
    RUN_ID= '93171fded89c469ba246e1432521682c'
    mlflow.artifacts.download_artifacts(run_id = RUN_ID, artifact_path = 'xgboost_time_series_energy.bin', dst_path='./downloads/')

    ```
    * Load artifacts from s3
    ```
    # Load model from S3
    RUN_ID= '55703e594fdc4cf2a3958502b7c10b9e'
    EXP_ID = 4  
    artifacts = f's3://mlflow-artifacts-evs/{EXP_ID}/{RUN_ID}/artifacts/xgboost_time_series_energy.bin'
    # Load the artifacts
    mlflow.artifacts.download_artifacts(artifact_uri = artifacts, dst_path='./downloads/')
    ```
    * Load model from s3
    ```
    RUN_ID= '55703e594fdc4cf2a3958502b7c10b9e'
    EXP_ID = 4  
    logged_model = f's3://mlflow-artifacts-evs/{EXP_ID}/{RUN_ID}/artifacts/models'
    model = mlflow.pyfunc.load_model(model_uri = logged_model, dst_path='./downloads/')

    ```

6. Run the flask via `python predict.py`

7. Run the test file via `python test.py`

**Note**:

* `docker ps -a` to lists all containers on your system, both running and stopped. .

* `docker exec -it image_name bash` to run a command in a running container.




