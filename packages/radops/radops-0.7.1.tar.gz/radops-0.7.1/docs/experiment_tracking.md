# Experiment Tracking

Currently, we support MLFlow as a backend for experiment tracking but provide a uniform interface for easily integrating additional backends, such as Chariot training v2 when it's ready. We adopt MLFlow terminiology which has the following notions:

- **Run** A single execution of a training script
- **Experiment** A collection of runs

## Setup

Using `radops config setup` you can configure the experiment tracking backend by providing the following information:

- MLFlow server URL
- MLFlow username
- MLFlow password

## Usage

The basic usage is as follows:

```python

from radops.tracking.mlflow import MLFlowRun

# creates or gets (if already exists) a run associated to an instance.
# `name` can be ommitted in which case a random name will be generated
run = MLFlowRun(experiment_name="my experiment", name="run name")

# log parameters (e.g. hyperparameters) one at a time or in bulk
run.log_param("param name", "param value")
run.log_params({"param name 1": "param value 1", "param name 2": "param value 2"})

# log metrics associated to a step one at a time or in bulk
run.log_metric("metric name", 0.5, step=3)
run.log_metrics({"metric name 1": 0.5, "metric name 2": 0.6}, step=7)

# mark the run as finished
run.end()

# retrive parameters
run.get_params()

# retrieve metrics
run.get_metrics()
```
