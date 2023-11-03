
class MLRunParameterKeys:
    _keys = []

    def __init__(self, keys: list[str]):
        self._keys = keys
    
    def __iter__(self):
        return iter(self._keys) if self._keys is not None else None

    def __len__(self):
        return len(self._keys) if self._keys is not None else 0

    def __contains__(self, key: str):
        return key in self._keys

    pass




class MLFlowParameters(MLRunParameterKeys):
    MLFlowUri = "ml.mlflow_uri"
    ExperimentName = "ml.experiment_name"
    ExperimentRunName = "ml.experiment_run_name"

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLFlowParameters, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        MLRunParameterKeys.__init__(self, 
                        [MLFlowParameters.MLFlowUri,
                        MLFlowParameters.ExperimentName,
                        MLFlowParameters.ExperimentRunName])
        pass

   


class GitParameters(MLRunParameterKeys):
    CodeGit = "ml.git_code"
    CodeGitCommit = "ml.git_code_commit"
    CodeGitIsDirty = "ml.git_code_is_dirty"
    DatasetGit = "ml.git_dataset"
    DatasetGitCommit = "ml.git_dataset_commit"
    DatasetGitIsDirty = "ml.git_dataset_is_dirty"


    def __init__(self, keys: list[str]):
        MLRunParameterKeys.__init__(self, 
                        [GitParameters.CodeGit,
                        GitParameters.CodeGitCommit,
                        GitParameters.CodeGitIsDirty,
                        GitParameters.DatasetGit,
                        GitParameters.DatasetGitCommit,
                        GitParameters.DatasetGitIsDirty
                        ] + keys)
        pass



_DATASET_PATH_PARAMETER_KEY = "ml.dataset_path"

class TrainRunParameters(GitParameters):
    ModelType = "ml.model_type"
    DatasetPath = _DATASET_PATH_PARAMETER_KEY

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TrainRunParameters, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        GitParameters.__init__(self, 
                        [TrainRunParameters.ModelType,
                        TrainRunParameters.DatasetPath])
        pass



class VerifyRunParameters(GitParameters):
    DatasetPath = _DATASET_PATH_PARAMETER_KEY

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VerifyRunParameters, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        GitParameters.__init__(self, [VerifyRunParameters.DatasetPath])
        pass


MLRUN_PARAM_MLFLOW = MLFlowParameters()
MLRUN_PARAM_TRAIN = TrainRunParameters()
MLRUN_PARAM_VERIFY = VerifyRunParameters()