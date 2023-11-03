from typing import TypeVar


TReleaseInfo = TypeVar("TReleaseInfo", bound = "ReleaseInfo")

class ReleaseInfo:

    @classmethod
    def latest_verify_run(cls, release_infos: list[TReleaseInfo]):
        latest_verify_run = None

        if len(release_infos) > 0:
            for item in release_infos:
                if latest_verify_run is None:
                    latest_verify_run = item.verify

                elif item.verify.info.end_time > latest_verify_run.info.end_time:
                    latest_verify_run = item.verify

        return latest_verify_run


    def __init__(self, name, model_type, model_version, verify, train):
        self._name = name
        self._type = model_type
        self._model_version = model_version
        self._verify = verify
        self._train = train
        pass

    @property
    def name(self):
        """String.  Model version name."""
        return self._name

    @property
    def type(self):
        """String.  Model type."""
        return self._type

    @property
    def model_version(self):
        """object.  Model version.  
        For MLFlow, returns :py:class:`mlflow.entities.model_registry.ModelVersion`.
        """
        return self._model_version

    @property
    def verify(self):
        """object.  Verify run.
        For MLFlow, returns :py:class:`mlflow.entities.Run` object.
        """
        return self._verify

    @property
    def train(self):
        """object.  Train run.
        For MLFlow, returns :py:class:`mlflow.entities.Run` object.
        """
        return self._train



    def __repr__(self):
        summary = (f"name: {self._name}\r\n"
                   f"model_version.version: {self._model_version.version}\r\n"
                   f"verify.info.run_name: {self._verify.info.run_name}\r\n"
                   f"verify.info.run_id: {self._verify.info.run_id}\r\n"
                   f"verify.info.experiment_id: {self._verify.info.experiment_id}\r\n"
                   f"train.info.run_name: {self._train.info.run_name}\r\n"
                   f"train.info.run_id: {self._train.info.run_id}\r\n"
                   f"train.info.experiment_id: {self._train.info.experiment_id} \r\n"
                   )
        
        return summary