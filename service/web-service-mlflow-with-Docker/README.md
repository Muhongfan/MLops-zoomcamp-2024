# Set up the web service with could & docker 

1. Create the folder "web-service". The tree of the folder is 
```
(base) (web-service-mlflow) amberm@Ambers-Air-2 web-service-mlflow % tree
.
├── Dockerfile
├── Pipfile
├── Pipfile.lock
├── README.md
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
├── predict.py
└── test.py
```

2. Build the docker
`docker build -t energy-consumption-prediction-service-mlflow:v1 .`
3. Run the docker
`docker run -v ~/.aws:/root/.aws:ro -p 9696:9696 energy-consumption-prediction-service-mlflow:v1`

**Note:**

`docker run -e RUN_ID=your_run_id -e EXP_ID=your_exp_id -e AWS_PROFILE=your_aws_profile -v ~/.aws:/root/.aws:ro -p 9696:9696 your-image-name`

4. Run the test file via `python test.py`

**Note**:

* `docker logs -f` to show the realtime logs .





