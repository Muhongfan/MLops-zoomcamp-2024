# Set up the web service on could & docker 

1. Under the folder [service](service/web-service-mlflow-with-Docker). The tree of the folder is 
```
├── aws_utils
├── data
├── mlops
├── service
    ├── web-service-mlflow-with-Docker
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── downloads
    │   │   └── models
    │   │       ├── MLmodel
    │   │       ├── conda.yaml
    │   │       ├── model.pkl
    │   │       ├── python_env.yaml
    │   │       └── requirements.txt
    │   ├── predict.py
    │   └── test.py
    └── monitoring

```
* `aws_utils`: upload config file and dataset that are used for workflow with mageai; 
* `data`: dataset
* `mlops`: workflow with mageai
* `service`: webservice and monitoring service

2. Build the docker for webservice under `service/web-service-mlflow-with-Docker`

`docker build -t energy-consumption-prediction-service-mlflow:v1 .`
3. Run the docker

`docker run -v ~/.aws:/root/.aws:ro -p 9696:9696 energy-consumption-prediction-service-mlflow:v1`

    ```
    docker run -e RUN_ID=your_run_id -e EXP_ID=your_exp_id -e AWS_PROFILE=your_aws_profile -v ~/.aws:/root/.aws:ro -p 9696:9696 your-image-name
    ```
    to configure your run_id, experiment_id and AWS profile

4. Run the test file via `python test.py`

**Note**:

* `docker logs -f` to show the realtime logs .





