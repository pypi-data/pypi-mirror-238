import datetime
import json
from tkinter import CURRENT
import mlflow
import os
import unittest
import mlpylib
from mlpylib.entity.releaseinfo import ReleaseInfo


class Test_FullCycle(unittest.TestCase):

    class MockConfig:
        MODEL_TYPE = None
        EPOCHS = 100
        pass

    def _mock_train_argument(self):
        with open(os.path.join(os.path.dirname(__file__), "mock-train-args.txt"), "r") as f:
            args = json.load(f)

        return ["--OVERRIDE_PARAMS", json.dumps(args)] 

    def _mock_verify_argument(self):
        with open(os.path.join(os.path.dirname(__file__), "mock-verify-args.txt"), "r") as f:
            args = json.load(f)

        return ["--OVERRIDE_PARAMS", json.dumps(args)] 

    def _create_dummy_model(self, model_file_path: str):
        if not os.path.exists(model_file_path):
            model_file_folder = os.path.dirname(model_file_path)

            if not os.path.exists(model_file_folder):
                os.mkdir(model_file_folder)

            with open(model_file_path, "w") as f:
                f.write("#dummy mock model#")

        pass


    @unittest.skip("for dev.")
    def test_fullcycle_train(self):
        try:
            mock_args = self._mock_train_argument()
        
            mock_config = Test_FullCycle.MockConfig()

            mlpylib.setup(mock_args)
            mlpylib.override_parameters(mock_config)
 
            mlflow.set_tracking_uri(mlpylib.mlrun_parameters[mlpylib.MLRUN_PARAM_MLFLOW.MLFlowUri])
            (environment, project_name, model_type) = mlpylib.explain_experiment_name()

            last_release_info = mlpylib.get_last_release_info(project_name, model_type)
            print(last_release_info)
        

            last_model_path = os.path.join(os.path.dirname(__file__), "./bin/last_version")
            if last_release_info is not None:
                mlflow.artifacts.download_artifacts(artifact_uri = last_release_info.model_version.source,
                                                    dst_path = last_model_path)


            experiment = mlflow.set_experiment("unittest_mlpylib")
            run_name = f'test_fullcycle_train_{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
            run_id = None
            with mlflow.start_run(run_name = run_name) as run:
                mlpylib.log_return_mlflow_info(experiment, run)
            
                mlpylib.log_standard_parameters()
                mlpylib.log_parameters(mock_config)

                model_file = os.path.join(os.path.dirname(__file__), "bin/mock_model.pth")
                self._create_dummy_model(model_file)

                mlpylib.log_model(model_file, mock_config.MODEL_TYPE, True)
                mlpylib.log_code()

        except Exception as error:
            mlpylib.log_return_error(error)
            pass

        mlpylib.wrapup_return()

        pass



    @unittest.skip("for dev.")
    def test_fullcycle_verify(self):
        try:
            mock_args = self._mock_verify_argument()
        
            mock_config = Test_FullCycle.MockConfig()

            mlpylib.setup(mock_args)
            mlpylib.override_parameters(mock_config)

            mlflow.set_tracking_uri(mlpylib.mlrun_parameters[mlpylib.MLRUN_PARAM_MLFLOW.MLFlowUri])
            (environment, project_name, _) = mlpylib.explain_experiment_name()



            crack_release_info = mlpylib.get_last_release_info(project_name, "crack")
            print(crack_release_info)

            grind_release_info = mlpylib.get_last_release_info(project_name, "grind")
            print(grind_release_info)

            last_release_verify_run = ReleaseInfo.latest_verify_run([grind_release_info, crack_release_info])

            last_model_path = os.path.join(os.path.dirname(__file__), "./bin/last_version")
            last_crack_pth = mlflow.artifacts.download_artifacts(artifact_uri = crack_release_info.model_version.source,
                                                dst_path = last_model_path)
            last_grind_pth = mlflow.artifacts.download_artifacts(artifact_uri = grind_release_info.model_version.source,
                                                dst_path = last_model_path)



            current_model_path = os.path.join(os.path.dirname(__file__), "./bin/current")

            model_artifacts = mlflow.MlflowClient().list_artifacts(run_id = mlpylib.mlrun_parameters.model_run_id("crack"), path = "model")
            current_crack_pth = mlflow.artifacts.download_artifacts(run_id = mlpylib.mlrun_parameters.model_run_id("crack"),
                                                artifact_path = model_artifacts[0].path,
                                                dst_path = os.path.join(current_model_path, "current_crack"))

            model_artifacts = mlflow.MlflowClient().list_artifacts(run_id = mlpylib.mlrun_parameters.model_run_id("grind"), path = "model")
            current_grind_pth = mlflow.artifacts.download_artifacts(run_id = mlpylib.mlrun_parameters.model_run_id("grind"),
                                                artifact_path = model_artifacts[0].path,
                                                dst_path = os.path.join(current_model_path, "current_grind"))



            experiment = mlflow.set_experiment("unittest_mlpylib")
            run_name = f'test_fullcycle_verify_{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
            run_id = None
            with mlflow.start_run(run_name = run_name) as run:
                mlpylib.log_return_mlflow_info(experiment, run)
            
                mlpylib.log_standard_parameters()
                mlpylib.log_parameters(mock_config)

                mlpylib.log_model(current_crack_pth, "crack", mlpylib.mlrun_parameters.is_model_run_new_train("crack"))
                mlpylib.log_model(current_grind_pth, "grind", mlpylib.mlrun_parameters.is_model_run_new_train("grind"))
                mlpylib.log_code()

        except Exception as error:
            mlpylib.log_return_error(error)
            pass

        mlpylib.wrapup_return()

        pass




if __name__ == "__main__":
    unittest.main()