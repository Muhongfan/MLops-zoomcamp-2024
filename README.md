# Energy Consumption Prediction for EV Charging Sessions

## **Project Objective:**
To develop a predictive model for estimating energy consumption during electric vehicle (EV) charging sessions using historical data from a workplace charging program. The model will aid in optimizing energy management, understanding usage patterns, and improving the efficiency of charging infrastructure.

## **Dataset Description:**
The dataset comprises 3,395 high-resolution EV charging sessions, with data collected from 85 EV drivers across 105 stations located at 25 different workplace sites. These sites include various facilities such as research and innovation centers, manufacturing plants, testing facilities, and office headquarters. The dataset is in CSV format, with timestamps recorded to the nearest second, allowing for precise analysis.

## **Key Features:**
- **sessionId:** Unique identifier for each charging session.
- **kwhTotal:** The amount of energy consumed during the session (in kWh).
- **dollars:** The amount of money paid for energy charging.
- **created:** Timestamp for when the charging session started.
- **end:** Timestamp for when the charging session ended.- **dollars:** The amount of money paid for energy charging.
- **startTime:** The min of the created time.
- **endTime:** The min of the end time.
- **chargeTimeHrs:** The total charging mins.
- **weekday:** Indicates if the session occurred on a weekday.
- **platform:** The platform used for accessing the Charging.
- **distance:** The distance from a user's home to the charging location, expressed in miles except where user did not report address..
- **userId:** Unique identifier for each user.
- **stationId:** Unique identifier for each station.
- **locationId:** Unique identifier for each location.
- **managerVehicle:** A ambiguous identifier which is described as "Firm manager vehicle indicator".
- **facilityType:** The type of facility a station is installed at (manufacturing = 1, office = 2, research and development = 3, other = 4). As indicated in the dataset description, all facility types are at workplaces..
- **reportedZip:** A ambiguous identifier for the Zip of the reported location.

## **Project Phases:**
1. **Exploratory Data Analysis (EDA):**
   - Conduct EDA to understand the distribution of energy consumption, session durations, and other relevant features.
   - Identify patterns, trends, and correlations within the data.
   
2. **Data Preprocessing for modeling:**
   - Clean and preprocess the data, handling any missing or inconsistent values.
   - Feature engineering to create additional relevant features such as `station_location` identifier.
   - Normalize and transform data as needed for model input.

3. **Model Development:**
   - Split the data into training and testing sets.
   - Develop predictive models using machine learning algorithms such as Linear Regression, Random Forest, or Gradient Boosting.
   - Fine-tune model parameters using cross-validation techniques to optimize performance.

4. **Model Evaluation:**
   - Evaluate the models using metrics such as Root Mean Squared Error (RMSE), and R-squared.
   - Select the best-performing model for deployment.

5. **Model Deployment:**
   - Deploy the predictive model, dataset, service on AWS S3, EC2 Instance, RDS.
   - Dockerized the online web service.
   - Set up a monitoring system to track model performance and retrain it with Evidently AI, Grafana and PostgreSQL.

This project will contribute to the ongoing efforts in optimizing EV charging infrastructure and support sustainable energy management practices in workplace environments.

## The projects details
1. **EDA and Data preprocessing**
The primary goal of the first step is to gain a basic understanding of the dataset related to energy consumption during electric vehicle (EV) charging sessions. Additionally, the analysis will explore and identify relationships between key variables such as energy consumption, associated costs, distance traveled, charge time, and user behavior.

All details are in [EDA for energy consumption dataset](project/EVs.ipynb)

## Modelling and tracking
The next step involves building the modeling process based on the exploration and setting up an experiment tracking pipeline using MLflow. The entire service will be deployed on AWS, utilizing EC2 for the tracking server, RDS for metadata storage, and an S3 bucket for storing datasets and models. Deployment will be managed using Docker to ensure consistency and scalability across the environment. This setup will streamline model experimentation and tracking, enhancing the efficiency of the development workflow.

All details are in [the web service for energy consumption prediction project](project/service/web-service-mlflow-with-Docker)

### **Setup**: 
#### Environment preparetion
* Using conda
1. Clone the repository:
   
`https://github.com/Muhongfan/MLops-zoomcamp-2024.git`

2. Navigate to Project directory

` cd project`

3. Create and activate the conda environment using the `environment.yml` file:

`
conda env create -f environment.yml
conda activate mlopsproject
`

* Using Pip
1. Clone the repository:
   
`https://github.com/Muhongfan/MLops-zoomcamp-2024.git`

2. Navigate to Project directory

` cd project`

3. Install the required packages using `requirements.txt`:

`pip install -r requirements.txt
`
#### Docker build up

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









## Orchestration
Using mage AI for ML workflow.

![Data preparetion pipeline](images/projects/pipeline-dataprepare.png)

### Setup
1. Jump to folder `mlops/` and start the service with `./scripts/start.sh`

2. Open `http://localhost:6789` in your browser.


### Monitoring results (some)
![The results of monitoring for datasets](images/projects/monitoring-datasets.png)
![The results of monitoring for chargeTimeHrs](images/projects/monitoring-chargeTimeHrs.png)
