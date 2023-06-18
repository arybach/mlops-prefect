import os
import pickle
import click
import mlflow
import optuna
import uuid

from optuna.samplers import TPESampler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

mlflow.set_tracking_uri("http://mlflow_mlops:5000")
# experiment_name = f"random-forest-hyperopt-{uuid.uuid4().hex}"
experiment_name = f"random-forest-hyperopt"
mlflow.set_experiment(experiment_name)


def load_pickle(filename):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="../output",
    help="Location where the processed NYC taxi trip data was saved"
)
@click.option(
    "--num_trials",
    default=10,
    help="The number of parameter evaluations for the optimizer to explore"
)
def run_optimization(data_path: str, num_trials: int):

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 10, 50, 1),
            'max_depth': trial.suggest_int('max_depth', 1, 20, 1),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 10, 1),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 4, 1),
            'random_state': 42,
            'n_jobs': -1
        }

        # mlflow.sklearn.autolog()

        rf = RandomForestRegressor(**params)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        
        # Log the validation RMSE to MLflow
        with mlflow.start_run():
            mlflow.log_params(params)
            mlflow.log_metric('rmse', rmse)

        return rmse

    sampler = TPESampler(seed=42)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(objective, n_trials=num_trials)

    # Get the best parameters and train the final model
    best_params = study.best_params
    final_rf = RandomForestRegressor(**best_params)
    final_rf.fit(X_train, y_train)
    
    # mlflow.sklearn.log_model(final_rf, artifact_path=f"s3://sparkhudi/mlflow/models/{experiment_name}.pkl")
    # Save the optimized model to a local file instead of built-in log_model
    model_path = f"../models/{experiment_name}"
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f_out:
       pickle.dump(final_rf, f_out)


if __name__ == '__main__':
    run_optimization()