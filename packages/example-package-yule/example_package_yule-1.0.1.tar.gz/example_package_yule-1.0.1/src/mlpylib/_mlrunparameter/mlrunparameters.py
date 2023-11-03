import argparse
import inspect
import json
import os
from typing import Any, Sequence


from mlpylib._mlops_platform.interface import (
    log_parameters,
    )
from mlpylib._mlrunparameter.mlrunparameterkeys import (
    GitParameters,
    MLRUN_PARAM_MLFLOW,
    MLRUN_PARAM_TRAIN,
    MLRUN_PARAM_VERIFY
    )
from mlpylib._util import (
    logging,
    nomenclature
    )
from mlpylib._util.gitutil import (
    GitInfo
    )


_logger = logging.get_logger()


class MLRunParameters:
    _INPUT_OVERRIDE_PARAMETERS = "OVERRIDE_PARAMS"
    _MLRUN_SYSTEM_PARAMETER_PREFIX = "ml."


    def __init__(self, args: Sequence[str] | None = None):
        self._initialize(args)
        pass

    def _initialize(self, args: Sequence[str] | None = None):
        parser = argparse.ArgumentParser()
        parser.add_argument(f"--{MLRunParameters._INPUT_OVERRIDE_PARAMETERS}", type=str, required=True)
        parsed_args = parser.parse_args() if args is None else parser.parse_args(args)

        self._parameters = json.loads(parsed_args.OVERRIDE_PARAMS)
        pass

    def set_experiment_run_name(self, run_name: str):
        current_value = self._parameters[MLRUN_PARAM_MLFLOW.ExperimentRunName]
        self._parameters[MLRUN_PARAM_MLFLOW.ExperimentRunName] = run_name
        print(f"set run name | current = '{current_value}' | new = '{run_name}'")
        pass


    def set_git_code_info(self, git_info: GitInfo):
        self._parameters[GitParameters.CodeGit] = git_info.url
        self._parameters[GitParameters.CodeGitCommit] = git_info.commit
        self._parameters[GitParameters.CodeGitIsDirty] = git_info.is_dirty
        pass


    def set_git_dataset_info(self, git_info: GitInfo):
        self._parameters[GitParameters.DatasetGit] = git_info.url
        self._parameters[GitParameters.DatasetGitCommit] = git_info.commit
        self._parameters[GitParameters.DatasetGitIsDirty] = git_info.is_dirty
        pass


    def set_verify_model_run_id(self, model_type: str, run_id: str):
        mlparamkey_run_id = nomenclature.the_paramkey_run_id(model_type)
        self._parameters[mlparamkey_run_id] = run_id
        pass




    def override_parameters(self, target: dict[str, Any] | object, insertIfNotExists: bool = False):
        if isinstance(target, dict):
            self._override_dict_value(target, insertIfNotExists)
        else:
            self._override_attribute_value(target, insertIfNotExists)
        pass

    def _override_dict_value(self, target: dict[str, Any], insertIfNotExists: bool):
        target_keys = {key.lower():key for key in target.keys()}

        if self._parameters is not None:
            for key, value in self._parameters.items():
                lookup_key = key[len(MLRunParameters._MLRUN_SYSTEM_PARAMETER_PREFIX):] if key.startswith(MLRunParameters._MLRUN_SYSTEM_PARAMETER_PREFIX) else key

                if lookup_key.lower() in target_keys:
                    target_original_key = target_keys[lookup_key.lower()]
                    old_value = target[target_original_key]
                    new_value = self._parameters[key]
                    target[target_original_key] = new_value
                    _logger.info(f"override '{target_original_key}' | old-value={old_value} | new-value={new_value}.")

                elif insertIfNotExists:
                    new_value = self._parameters[key]
                    target[lookup_key] = new_value
                    _logger.info(f"add new '{lookup_key}' | new-value={new_value}.")               
            
        pass
    
    def _override_attribute_value(self, target: object, insertIfNotExists: bool):
        target_attributes = {value.lower():value for value in dir(target)}

        if self._parameters is not None:
            for key, value in self._parameters.items():
                lookup_key = key[len(MLRunParameters._MLRUN_SYSTEM_PARAMETER_PREFIX):] if key.startswith(MLRunParameters._MLRUN_SYSTEM_PARAMETER_PREFIX) else key

                if lookup_key.lower() in target_attributes:
                    target_original_attribute = target_attributes[lookup_key.lower()]
                    old_value = getattr(target, target_original_attribute, lambda: None)
                    new_value = self._parameters[key]
                    setattr(target, target_original_attribute, value)
                    _logger.info(f"override '{target_original_attribute}' | old-value={old_value} | new-value={new_value}.")

                elif insertIfNotExists:
                    new_value = self._parameters[key]
                    setattr(target.__class__, lookup_key, value)
                    _logger.info(f"add new '{lookup_key}' | new-value={new_value}.")               
            
        pass



    def log_standard_parameters(self):
        parameters = {}
        logged_system_parameter_keys = []

        for key in self._parameters:
            if key.startswith(MLRunParameters._MLRUN_SYSTEM_PARAMETER_PREFIX) \
                and key not in MLRUN_PARAM_MLFLOW:
                parameters[key] = self._parameters[key]
    
        if len(parameters) > 0:
            log_parameters(parameters)

        pass



    def log_parameters(self, custom_config: dict[str, Any] | object):
        if isinstance(custom_config, dict):
            log_parameters(custom_config)    

        else:
            parameters = {}
            for key in dir(custom_config):
                if key.startswith("_") or type(getattr(custom_config, key)).__name__.startswith("method"): 
                    continue
                else:
                    parameters[key] = getattr(custom_config, key)

            log_parameters(parameters)

        pass




    def __getitem__(self, key: str):
        return self._parameters[key] if key in self._parameters else None

    def __len__(self):
        return 0 if self._parameters is None else len(self._parameters)

    def __contains__(self, key: str):
        return key in self._parameters


    def keys(self):
        return self._parameters.keys()