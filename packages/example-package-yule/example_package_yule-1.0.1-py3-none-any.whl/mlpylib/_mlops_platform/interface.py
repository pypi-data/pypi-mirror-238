from typing import Any

from mlpylib._mlops_platform.mlflowhandler import MLFlowHandler


_instance = None

def setup(platform_url: str):
    global _instance
    _instance = MLFlowHandler(platform_url)


def log_parameters(parameters: dict[str, Any]) -> None:
    global _instance
    _instance.log_parameters(parameters)
    pass


def log_code(source: str) -> None:
    global _instance
    _instance.log_code(source)
    pass


def log_model(source: str, target: str) -> None:
    global _instance
    _instance.log_model(source, target)
    pass


def get_model_version(model_version_name: str, stage: str):
    global _instance
    return _instance.get_model_version(model_version_name, stage)


def get_experiment_run(run_id: str):
    global _instance
    return _instance.get_experiment_run(run_id)



def get_experiment_run_by_name(experiment_name: str, run_name: str):
    global _instance
    return _instance.get_experiment_run_by_name(experiment_name, run_name)

