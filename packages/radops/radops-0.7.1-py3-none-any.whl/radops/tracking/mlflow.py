from mlflow import (
    MlflowException,
    create_experiment,
    delete_run,
    end_run,
    get_experiment_by_name,
    get_run,
    log_metric,
    log_metrics,
    log_param,
    log_params,
    search_runs,
    start_run,
)
from mlflow.exceptions import RestException

from radops.settings import setup_mlflow
from radops.tracking.base import Run


def create_or_get_experiment(name: str) -> str:
    """Creates or get an experiment by name, returning its id"""
    try:
        return create_experiment(name)
    except (MlflowException, RestException):
        return get_experiment_by_name(name).experiment_id


def create_or_get_run(experiment_name: str, name: str = None) -> str:
    """Creates or get a run by name, returning its id"""
    experiment_id = create_or_get_experiment(experiment_name)
    try:
        return start_run(
            experiment_id=experiment_id, run_name=name
        ).info.run_id
    except Exception as e:
        # get runs associated to the experiment
        runs = search_runs(
            experiment_ids=[experiment_id],
            filter_string=f"tags.mlflow.runName='{name}'",
            output_format="list",
        )

        if len(runs) != 1:
            raise Exception(
                f"Unexpected error: could not create run but no run with name {name} "
                f"in experiment {experiment_name} was found. Got exception {e}"
            )

        return runs[0].info.run_id


class MLFlowRun(Run):
    def __init__(self, experiment_name: str, name: str = None) -> None:
        setup_mlflow()
        self.run_id = create_or_get_run(
            experiment_name=experiment_name, name=name
        )

    def log_param(self, key: str, value: str) -> None:
        log_param(key, value)

    def log_params(self, params: dict) -> None:
        log_params(params)

    def log_metric(self, key: str, value: float, step: int = None) -> None:
        log_metric(key, value, step=step)

    def log_metrics(self, metrics: dict, step: int = None) -> None:
        log_metrics(metrics, step=step)

    def get_params(self) -> dict:
        return get_run(run_id=self.run_id).data.params

    def get_metrics(self) -> dict:
        return get_run(run_id=self.run_id).data.metrics

    def end(self) -> None:
        end_run()

    def delete(self) -> None:
        delete_run(self.run.info.run_id)
