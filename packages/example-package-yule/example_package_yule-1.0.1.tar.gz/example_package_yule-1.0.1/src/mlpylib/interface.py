import inspect
import json
import mlflow
import os
import re

from datetime import (
    datetime
    )
from typing import (
    Any,
    Optional,
    Sequence
    )
from xml.dom.expatbuilder import theDOMImplementation

import mlpylib._mlops_platform.interface as mlplatform
import mlpylib._mlrunparameter.mlrunparameterkeys as mlrunparameterkeys

from mlpylib._mlrunparameter.mlrunparameterkeys import (
    MLRUN_PARAM_MLFLOW
    )
from mlpylib._mlrunparameter.mlrunparameters import (
    MLRunParameters
    )
from mlpylib._util import (
    code,
    gitutil,
    nomenclature
    )
from mlpylib.entity.releaseinfo import (
    ReleaseInfo
    )



_DEFAULT_CODE_ARTIFACT_FILENAME = "ml-script.tar"
_DEFAULT_LOG_RETURN_FILE = "mlops_return.txt"
_LOG_RETURN_TAG_ERROR = "ml.error"
_LOG_RETURN_TAG_EXPERIMENT_NAME = "ml.experiment_name"
_LOG_RETURN_TAG_EXPERIMENT_ID = "ml.experiment_id"
_LOG_RETURN_TAG_RUN_NAME = "ml.run_name"
_LOG_RETURN_TAG_RUN_ID = "ml.run_id"

_active_mlrun_parameters = None
_active_mlrun_code_git = None
_active_mlrun_dataset_git = None
_active_mlrun_returns = None



class _MLRunParametersInterface:
    def __getitem__(self, key: str):
        global _active_mlrun_parameters
        return _active_mlrun_parameters[key]

    def __len__(self):
        global _active_mlrun_parameters
        return len(_active_mlrun_parameters)

    def __contains__(self, key: str):
        global _active_mlrun_parameters
        return key in _active_mlrun_parameters
    
    def model_run_name(self, model_type: str):
        global _active_mlrun_parameters
        param_key = nomenclature.the_paramkey_run_name(model_type)
        return _active_mlrun_parameters[param_key] \
                if param_key in _active_mlrun_parameters \
                else None
    
    def model_run_id(self, model_type: str):
        global _active_mlrun_parameters
        param_key = nomenclature.the_paramkey_run_id(model_type)
        return _active_mlrun_parameters[param_key] \
                if param_key in _active_mlrun_parameters \
                else None
    
    def model_run_state(self, model_type: str):
        global _active_mlrun_parameters
        param_key = nomenclature.the_paramkey_run_state(model_type)
        return _active_mlrun_parameters[param_key] \
                if param_key in _active_mlrun_parameters \
                else None

    def is_model_run_new_train(self, model_type: str):
        state = self.model_run_state(model_type)
        return state == nomenclature.RUN_STATE_NEW_TRAIN

    pass

mlrun_parameters = _MLRunParametersInterface()


def setup(args: Optional[Sequence[str]] = None):
    global _active_mlrun_parameters
    global _active_mlrun_returns

    _active_mlrun_parameters = MLRunParameters(args)
    _apply_run_name_with_timestamp()

    mlplatform.setup(_active_mlrun_parameters[MLRUN_PARAM_MLFLOW.MLFlowUri])

    frame_info = inspect.stack(0)[1]
    caller_code_folder = os.path.dirname(frame_info.filename)
    _setup_git_info(caller_code_folder)

    _setup_verify_info()

    _active_mlrun_returns = None

    pass


def _apply_run_name_with_timestamp():
    global _active_mlrun_parameters

    run_name = _active_mlrun_parameters[MLRUN_PARAM_MLFLOW.ExperimentRunName]
    if re.match(".+_[0-9]{8}_[0-9]{6}$", run_name) is None:
        _active_mlrun_parameters.set_experiment_run_name(f'{run_name}_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}')

    pass


def _setup_git_info(code_folder: str):
    global _active_mlrun_parameters
    global _active_mlrun_code_git
    global _active_mlrun_dataset_git

    _active_mlrun_code_git = gitutil.get_git_info(code_folder)
    _active_mlrun_parameters.set_git_code_info(_active_mlrun_code_git)
    
    _active_mlrun_dataset_git = gitutil.get_git_info(_active_mlrun_parameters[mlrunparameterkeys._DATASET_PATH_PARAMETER_KEY])
    _active_mlrun_parameters.set_git_dataset_info(_active_mlrun_dataset_git)
    pass


def _setup_verify_info():
    global _active_mlrun_parameters
    
    current_experiment_name = _active_mlrun_parameters[MLRUN_PARAM_MLFLOW.ExperimentName]

    if nomenclature.is_verify_experiment(current_experiment_name):

        (environment, project_name, _) = nomenclature.explain_experiment_name(current_experiment_name)
        run_name_pattern = nomenclature.the_paramkey_run_name_pattern()
        train_run_ids = []

        for key in [item for item in _active_mlrun_parameters.keys() if item not in MLRUN_PARAM_MLFLOW]:
            match = run_name_pattern.match(key)

            if match is not None:
                type = match[1]
                train_experiement_name = nomenclature.compute_experiment_name(environment, project_name, type)
                train_run_name = _active_mlrun_parameters[key]
                run = mlplatform.get_experiment_run_by_name(train_experiement_name, train_run_name)
                
                if run is not None:
                    run_id = run.info.run_id
                    _active_mlrun_parameters.set_verify_model_run_id(type, run_id)
                    train_run_ids.append(run_id)

        if len(train_run_ids) == 0:
            raise Exception("Verify experiment run must contain at least 1 train run.")

    pass    





def override_parameters(target: object | dict, insertIfNotExists: Optional[bool] = False):
    global _active_mlrun_parameters
    _active_mlrun_parameters.override_parameters(target, insertIfNotExists)
    pass



def log_standard_parameters():
    global _active_mlrun_parameters
    _active_mlrun_parameters.log_standard_parameters()
    pass



def log_parameters(custom_config: dict[str, Any] | object):
    global _active_mlrun_parameters
    _active_mlrun_parameters.log_parameters(custom_config)
    pass



def log_code():
    global _active_mlrun_code_git

    if _active_mlrun_code_git is None or _active_mlrun_code_git.working_tree_dir is None:
        raise Exception(f"Not a git repo and mlpylib.setup() is not called.")

    else:
        code_artifact_file = os.path.join(_active_mlrun_code_git.working_tree_dir, _DEFAULT_CODE_ARTIFACT_FILENAME)
        try:
            code_artifact_file = os.path.join(_active_mlrun_code_git.working_tree_dir, _DEFAULT_CODE_ARTIFACT_FILENAME)
            code.pack_code(_active_mlrun_code_git, code_artifact_file)        
            mlplatform.log_code(code_artifact_file)

        finally:
            if os.path.exists(code_artifact_file):
                os.remove(code_artifact_file)

    pass



def log_model(source: str, model_type: str, is_new_train: bool):
    global _active_mlrun_parameters

    (original_model_filename, file_extension) = os.path.splitext(source)
    model_artifact_path = nomenclature.compute_model_artifact_full_path(
                            _active_mlrun_parameters[MLRUN_PARAM_MLFLOW.ExperimentName],
                            model_type,
                            is_new_train) + file_extension

    mlplatform.log_model(source, model_artifact_path)
    pass



def get_last_release_info(project_name: str, model_type: str) -> ReleaseInfo:
    model_version_name = nomenclature.compute_model_version_name(project_name, model_type)
    paramkey_run_id = nomenclature.the_paramkey_run_id(model_type)

    model_version = mlplatform.get_model_version(model_version_name, "Production")
    verify_run = mlplatform.get_experiment_run(model_version.run_id)
    train_run = mlplatform.get_experiment_run(verify_run.data.params[paramkey_run_id])
    
    return ReleaseInfo(
            name = model_version_name, 
            model_type = model_type,
            model_version = model_version,
            verify = verify_run,
            train = train_run
            )



def get_experiment_run_by_name(project_name: str, run_name: str):
    return mlplatform.get_experiment_run_by_name(project_name, run_name)



def explain_experiment_name(experiment_name: Optional[str] = None) -> tuple[str, str, str]:
    """
    Explain experiment name into environment, project name and model train/verify type.

    :param name: Experiment name.
    :return: Environment.
    :return: Project name.
    :return: Model train/verify type.
    """
    global _active_mlrun_parameters

    if experiment_name is None:
        current_experiment_name = _active_mlrun_parameters[MLRUN_PARAM_MLFLOW.ExperimentName]
        return nomenclature.explain_experiment_name(current_experiment_name)

    else:
        return nomenclature.explain_experiment_name(experiment_name)

    pass


def explain_model_artifact_name(model_artifact_name: str) -> tuple[str, str]:
    return nomenclature.explain_model_artifact_name(model_artifact_name)





def log_return(key: str, value: str):
    global _active_mlrun_returns

    if _active_mlrun_returns is None:
        _active_mlrun_returns = {}

    if key in _active_mlrun_returns:
        _active_mlrun_returns[key] += value
    else:
        _active_mlrun_returns[key] = value

    pass




def log_return_error(error: str):
    log_return(_LOG_RETURN_TAG_ERROR, error)


def log_return_mlflow_info(experiment: Optional[mlflow.entities.Experiment] = None, 
                    run: Optional[mlflow.entities.Run] = None):

    if experiment is not None:
        log_return(_LOG_RETURN_TAG_EXPERIMENT_NAME, experiment.name)
        log_return(_LOG_RETURN_TAG_EXPERIMENT_ID, experiment.experiment_id)

    if run is not None:
        log_return(_LOG_RETURN_TAG_RUN_NAME, run.info.run_name)
        log_return(_LOG_RETURN_TAG_RUN_ID, run.info.run_id)

    pass



def wrapup_return():
    global _active_mlrun_returns

    frame_info = inspect.stack(0)[1]
    caller_code_folder = os.path.dirname(frame_info.filename)

    return_file = os.path.join(caller_code_folder, _DEFAULT_LOG_RETURN_FILE)
    with open(return_file, "w") as f:
        json.dump(_active_mlrun_returns, f)

    pass