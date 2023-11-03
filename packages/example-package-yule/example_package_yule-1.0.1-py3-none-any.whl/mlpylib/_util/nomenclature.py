import re

RUN_STATE_NEW_TRAIN = "TRAIN"
RUN_STATE_NEW_REUSE = "REUSE"

_NEW_MODEL_ARTIFACT_PREFIX = "model"
_REUSE_MODEL_ARTIFACT_PREFIX = "reusemodel"


def compute_experiment_name(environment: str, project_name: str, run_type: str):
    return f"{environment}_{project_name}_{run_type}"


def explain_experiment_name(name: str) -> tuple[str, str, str]:
    name_tokens = name.split("_")
    environment = name_tokens[0] if len(name_tokens) >= 1 else None
    project_name = name_tokens[1] if len(name_tokens) >= 2 else None
    model_type = name_tokens[2] if len(name_tokens) >= 3 else None

    return (environment, project_name, model_type)



def compute_model_artifact_name(experiment_name: str, model_type: str) -> str:
    (_, project_name, _) = explain_experiment_name(experiment_name)

    return f"{project_name}_{model_type}"


def explain_model_artifact_name(model_artifact_name: str) -> tuple[str, str]:
    name_tokens = model_artifact_name.split("_")
    project_name = name_tokens[0] if len(name_tokens) >= 1 else None
    model_type = name_tokens[1] if len(name_tokens) >= 2 else None
    return (project_name, model_type)



def compute_model_artifact_full_path(experiment_name: str, model_type: str, is_new_train: bool) -> str:
    model_artifact_name = compute_model_artifact_name(experiment_name, model_type)

    return f"{_NEW_MODEL_ARTIFACT_PREFIX}/{model_artifact_name}" \
            if is_new_train \
            else f"{_REUSE_MODEL_ARTIFACT_PREFIX}/{model_artifact_name}"



def compute_model_version_name(project_name: str, model_type: str) -> str:
    return f"{project_name}_{model_type}"



def is_verify_experiment(experiment_name: str) -> bool:
    return experiment_name.endswith("_verify")


def the_paramkey_run_id(model_type: str) -> str:
    return f"ml.{model_type}_runid"


def the_paramkey_run_name(model_type: str) -> str:
    return f"ml.{model_type}_run"


def the_paramkey_run_name_pattern() -> re.Pattern:
    return re.compile("^ml\\.([a-zA-Z]+)_run$")


def the_paramkey_run_state(model_type: str) -> str:
    return f"ml.{model_type}_state"
