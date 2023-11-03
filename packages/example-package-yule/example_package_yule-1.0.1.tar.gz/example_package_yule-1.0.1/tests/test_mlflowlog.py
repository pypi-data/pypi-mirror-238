import datetime
import json
import mlflow
import os
import unittest
import mlpylib


class Test_MLFlowLog(unittest.TestCase):

    class MockConfig:
        MODEL_TYPE = None
        EPOCHS = 100
        pass

    mock_config_dict = { "MODEL_TYPE": None, "EPOCHS": 100 }

    def _mock_train_argument(self):
        with open(os.path.join(os.path.dirname(__file__), "mock-train-args.txt"), "r") as f:
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



    #@unittest.skip("for dev.")
    def test_log_standard_params(self):
        mock_args = self._mock_train_argument()

        mlpylib.setup(mock_args)
        
        mlflow.set_tracking_uri(mlpylib.mlrun_parameters[mlpylib.MLRUN_PARAM_MLFLOW.MLFlowUri])
        mlflow.set_experiment("unittest_mlpylib")
        run_name = f'test_log_standard_params_{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
        run_id = None
        with mlflow.start_run(run_name = run_name) as run:
            run_id = run.info.run_id
            mlpylib.log_standard_parameters()


        run = mlflow.get_run(run_id)
        assert len(run.data.params) == len(mlpylib.MLRUN_PARAM_TRAIN)
        assert run.data.params[mlpylib.MLRUN_PARAM_TRAIN.CodeGit] == mlpylib.mlrun_parameters[mlpylib.MLRUN_PARAM_TRAIN.CodeGit]

        pass



    #@unittest.skip("for dev.")
    def test_log_config_object(self):
        mock_args = self._mock_train_argument()
        mock_config = Test_MLFlowLog.MockConfig()

        mlpylib.setup(mock_args)
        mlpylib.override_parameters(mock_config)

        mlflow.set_tracking_uri(mlpylib.mlrun_parameters[mlpylib.MLRUN_PARAM_MLFLOW.MLFlowUri])
        mlflow.set_experiment("unittest_mlpylib")
        run_name = f'test_log_config_object_{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
        run_id = None
        with mlflow.start_run(run_name = run_name) as run:
            run_id = run.info.run_id
            mlpylib.log_parameters(mock_config)


        run = mlflow.get_run(run_id)
        assert len(run.data.params) == 2
        assert run.data.params["MODEL_TYPE"] == mock_config.MODEL_TYPE

        pass



    #@unittest.skip("for dev.")
    def test_log_config_dict(self):
        mock_args = self._mock_train_argument()
        mock_config = Test_MLFlowLog.mock_config_dict.copy()

        mlpylib.setup(mock_args)
        mlpylib.override_parameters(mock_config)

        mlflow.set_tracking_uri(mlpylib.mlrun_parameters[mlpylib.MLRUN_PARAM_MLFLOW.MLFlowUri])
        mlflow.set_experiment("unittest_mlpylib")
        run_name = f'test_log_config_dict_{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
        run_id = None
        with mlflow.start_run(run_name = run_name) as run:
            run_id = run.info.run_id
            mlpylib.log_parameters(mock_config)


        run = mlflow.get_run(run_id)
        assert len(run.data.params) == 2
        assert run.data.params["MODEL_TYPE"] == mock_config["MODEL_TYPE"]

        pass



    #@unittest.skip("for dev.")
    def test_log_code(self):
        mock_args = self._mock_train_argument()

        mlpylib.setup(mock_args)
        
        mlflow.set_tracking_uri(mlpylib.mlrun_parameters[mlpylib.MLRUN_PARAM_MLFLOW.MLFlowUri])
        mlflow.set_experiment("unittest_mlpylib")
        run_name = f'test_log_code_{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
        run_id = None
        with mlflow.start_run(run_name = run_name) as run:
            run_id = run.info.run_id
            mlpylib.log_code()

        artifacts = mlflow.MlflowClient().list_artifacts(run_id)
        assert len(artifacts) == 1
        assert artifacts[0].path == "ml-script.tar"
        pass


    #@unittest.skip("for dev.")
    def test_log_model(self):
        mock_args = self._mock_train_argument()

        mlpylib.setup(mock_args)
        
        try:
            mlflow.set_tracking_uri(mlpylib.mlrun_parameters[mlpylib.MLRUN_PARAM_MLFLOW.MLFlowUri])
            mlflow.set_experiment("unittest_mlpylib")
            run_name = f'test_log_model_{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
            run_id = None
            with mlflow.start_run(run_name = run_name) as run:
                run_id = run.info.run_id

                model_file = os.path.join(os.path.dirname(__file__), "bin/mock_model.pth")
                self._create_dummy_model(model_file)

                mlpylib.log_model(model_file, "crack", True)
                mlpylib.log_model(model_file, "grind", False)

            artifacts = mlflow.MlflowClient().list_artifacts(run_id)
            assert len(artifacts) == 2
            #assert artifacts[0].path == "ml-script.tar"

        finally:
            if os.path.exists(model_file):
                os.remove(model_file)        


        pass



if __name__ == "__main__":
    unittest.main()