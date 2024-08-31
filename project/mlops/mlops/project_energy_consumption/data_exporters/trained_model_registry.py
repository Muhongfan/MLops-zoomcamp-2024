import mlflow
import os
import pickle
import boto3
import pandas as pd
# from mlflow.tracking import MlflowClient
from mlflow.models import infer_signature
from xgboost import XGBRegressor  # Ensure you import the correct class

from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
os.environ["AWS_PROFILE"] = "mac2aws"

# Initialize a session using Amazon S3
session = boto3.Session(profile_name="mac2aws")

# Retrieve the credentials
credentials = session.get_credentials()

# Set the credentials as environment variables
if credentials:
    os.environ["AWS_ACCESS_KEY_ID"] = credentials.access_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = credentials.secret_key
    
    # Set the session token if available
    if credentials.token:
        os.environ["AWS_SESSION_TOKEN"] = credentials.token
    
    # Set the default region if available
    if session.region_name:
        os.environ["AWS_DEFAULT_REGION"] = session.region_name

    print("Credentials are set as environment variables")
else:
    print("Credentials not available")

TRACKING_SERVER_HOST = os.getenv('TRACKING_SERVER_HOST') 
MLFLOW_PORT = os.getenv('MLFLOW_PORT') 
EXPERIMENT_NAME = os.environ.get("EXPERIMENT_NAME")
REGISTERED_MODEL_NAME =  os.getenv('REGISTERED_MODEL_NAME')
mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:{MLFLOW_PORT}")
mlflow.set_experiment(EXPERIMENT_NAME)
mlflow.sklearn.autolog()

@data_exporter
def export_data(data,data2, *args, **kwargs) -> str:

    model, hyperparameters, _ = data['xgboost']
    X, _, _, y, _, _, dv = data2['build']
    df_train, df_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Convert DataFrame rows to dictionaries
    df_train_dicts = df_train.to_dict(orient='records')
    df_test_dicts = df_test.to_dict(orient='records')
    os.makedirs('models', exist_ok=True)
    artifact_uri = ''
    run_id = ''

    with mlflow.start_run() as run:
        # basic info
        mlflow.set_tag("ML Engineer", "Amber Mu")
        mlflow.log_param("model_type", "XGBRegressor")
        mlflow.log_params(hyperparameters)

        pipeline = make_pipeline(
            DictVectorizer(),
            XGBRegressor(**hyperparameters, n_jobs=-1)
        )
        pipeline.fit(df_train_dicts, y_train)
        y_pred = pipeline.predict(df_test_dicts)

        # Log the training and test datasets
        train_df = pd.DataFrame(df_train, columns=df_train.columns)
        train_df['target'] = y_train

        test_df = pd.DataFrame(df_test, columns=df_test.columns)
        test_df['target'] = y_test

        with open("models/train_df.pkl", "wb") as f_out:
            pickle.dump(train_df, f_out)
        mlflow.log_artifact("models/train_df.pkl", artifact_path="datasets/training")

        with open("models/test_df.pkl", "wb") as f_out:
            pickle.dump(test_df, f_out)
        mlflow.log_artifact("models/test_df.pkl", artifact_path="datasets/testing")

        # Log the model
        mlflow.sklearn.log_model(pipeline, artifact_path="models")

        signature = infer_signature(df_test, y_pred)
        # Log Model
        model_info = mlflow.sklearn.log_model(
            sk_model=model, 
            artifact_path="models",
            registered_model_name= REGISTERED_MODEL_NAME,
            signature=signature
        )
        
        artifact_uri = mlflow.get_artifact_uri()
        run_id = run.info.run_id
        print(f"default artifact URI: '{artifact_uri}'")
        print(f"RunID: '{run.info.run_id}'")
        # Predict

        # Calculate and log metrics
        rmse = mean_squared_error(y_pred, y_test, squared=False)
        r2 = r2_score(y_test, y_pred)

        mlflow.log_metric('rmse', rmse)
        mlflow.log_metric("r2", r2)
    
    # Register Model
    # client = MlflowClient(TRACKING_URI)
    logged_model = f"runs:/{run_id}/models"
    mlflow.register_model(logged_model, f"{EXPERIMENT_NAME}")

    return logged_model, artifact_uri, run_id