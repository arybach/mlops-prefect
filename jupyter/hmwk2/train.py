import os
import pickle
import click
import mlflow
import uuid

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option("--data_path", default="output", help="Location where the processed NYC taxi trip data was saved")
@click.option("--experiment_name", default=f"nyc-taxi-experiment", help="Name of the MLflow experiment")
@click.option("--metaflow_url", default="http://mlflow_mlops:5000", help="URL of the MLflow tracking server")
@click.option("--storage_url", default="s3://sparkhudi/mlflow", help="Storage location")
def run_train(data_path: str, experiment_name: str, metaflow_url: str, storage_url: str):
    mlflow.set_tracking_uri(metaflow_url)
    mlflow.create_experiment(experiment_name, storage_url)
    mlflow.set_experiment(experiment_name)

    mlflow.sklearn.autolog()
    mlflow.set_tag("dev", "groot")
    mlflow.log_param("train-data-path", data_path)

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    rf = RandomForestRegressor(max_depth=10, random_state=0)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_val)

    rmse = mean_squared_error(y_val, y_pred, squared=False)
    mlflow.log_metric("rmse", rmse)

    # Save the trained model to a local file
    model_path = f"../models/{experiment_name}"
    # os.makedirs(os.path.dirname(model_path), exist_ok=True)

    with open('model.bin', 'wb') as f_out:
        pickle.dump((X_train, y_train, rf), f_out)

    mlflow.log_artifact('model.bin', artifact_path=model_path)

if __name__ == "__main__":
    run_train()
