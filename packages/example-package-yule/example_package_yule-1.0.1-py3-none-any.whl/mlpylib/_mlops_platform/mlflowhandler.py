import mlflow
import os
import shutil

from typing import Any

from mlpylib._util import (
    logging
	)
from mlpylib.entity.releaseinfo import (
	ReleaseInfo
	)

_logger = logging.get_logger()


class MLFlowHandler:	
	def __init__(self, platform_url: str):
		mlflow.set_tracking_uri(platform_url)
		pass
	

	def log_parameters(self, parameters: dict[str, Any]) -> None:
		global _logger

		_logger.info(parameters)
		mlflow.log_params(parameters)
		pass

	def log_code(self, source: str) -> None:
		global _logger

		_logger.info(source)
		mlflow.log_artifact(source)
		pass

	def log_model(self, source: str, target: str) -> None:
		global _logger

		source_name = os.path.basename(source)
		target_name = os.path.basename(target)
		target_dir = os.path.dirname(target)

		need_rename_model_file = source_name != target_name
		upload_file = os.path.join(os.path.dirname(source), target_name) if need_rename_model_file else source

		try:
			if need_rename_model_file:
				shutil.copy(source, upload_file)     

			mlflow.log_artifact(upload_file, target_dir)

		finally:
			if need_rename_model_file and os.path.exists(upload_file):
				os.remove(upload_file)

		pass
	


	def get_model_version(self, model_version_name: str, stage: str) -> mlflow.entities.model_registry.ModelVersion:
		model_versions = mlflow.MlflowClient().get_latest_versions(model_version_name, stages = [stage])  
		return model_versions[0] if model_versions is not None and len(model_versions) == 1 else None



	def get_experiment_run(self, run_id: str) -> mlflow.entities.Run:
		return mlflow.get_run(run_id)



	def get_experiment_run_by_name(self, experiment_name: str, run_name: str) -> mlflow.entities.Run:
		found_runs = mlflow.search_runs(
						experiment_names = [experiment_name],
						filter_string = f"attributes.run_name = '{run_name}'",
						output_format = "list")

		return found_runs[0] if found_runs is not None and len(found_runs) ==  1 else None
