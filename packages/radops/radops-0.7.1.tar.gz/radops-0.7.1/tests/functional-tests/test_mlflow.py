import datetime

import pytest
from mlflow import delete_experiment, get_experiment_by_name

from radops.tracking.mlflow import MLFlowRun


@pytest.fixture
def experiment_name() -> str:
    # create experiment name with current datetime
    exp_name = f"radops-integration-test-{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
    yield exp_name
    delete_experiment(get_experiment_by_name(exp_name).experiment_id)


def test_mlflow_run(experiment_name: str):
    run = MLFlowRun(experiment_name=experiment_name, name="test run")
    run.log_param("param1", "value1")
    run.log_params({"param2": "value2", "param3": "value3"})
    run.log_metric("metric1", 1.0, step=1)
    run.log_metrics({"metric2": 2.5, "metric3": 3.1}, step=2)

    expected_params = {
        "param1": "value1",
        "param2": "value2",
        "param3": "value3",
    }
    expected_metrics = {"metric1": 1.0, "metric2": 2.5, "metric3": 3.1}

    assert run.get_params() == expected_params
    assert run.get_metrics() == expected_metrics

    # check we can get the run again and get the same params and metrics
    run = MLFlowRun(experiment_name=experiment_name, name="test run")
    assert run.get_params() == expected_params
    assert run.get_metrics() == expected_metrics

    # check we can end a run
    run.end()
