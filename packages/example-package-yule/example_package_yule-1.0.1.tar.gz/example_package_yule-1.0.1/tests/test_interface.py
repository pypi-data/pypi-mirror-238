import json
import os
import unittest
import mlpylib


class Test_Interface(unittest.TestCase):

    class MockConfig:
        MODEL_TYPE = None
        EPOCHS = 100
        pass

    mock_config_dict = { "MODEL_TYPE": None, "EPOCHS": 100 }

    def _mock_train_argument(self):
        with open(os.path.join(os.path.dirname(__file__), "mock-train-args.txt"), "r") as f:
            args = json.load(f)

        return ["--OVERRIDE_PARAMS", json.dumps(args)] 



    #@unittest.skip("for dev.")
    def test_setup(self):
        mock_args = self._mock_train_argument()

        mlpylib.setup(mock_args)
        assert len(mlpylib.interface.mlrun_parameters) == 12
        pass



    #@unittest.skip("for dev.")
    def test_override_parameters_with_object(self):
        mock_args = self._mock_train_argument()
        mock_config = Test_Interface.MockConfig()

        mlpylib.setup(mock_args)
        mlpylib.override_parameters(mock_config)

        assert mock_config.EPOCHS == 80
        assert mock_config.MODEL_TYPE == "crack"
        pass


    #@unittest.skip("for dev.")
    def test_override_parameters_insert_new_with_object(self):
        mock_args = self._mock_train_argument()
        mock_config = Test_Interface.MockConfig()

        mlpylib.setup(mock_args)
        mlpylib.override_parameters(mock_config, True)

        assert mock_config.EPOCHS == 80
        assert mock_config.MODEL_TYPE == "crack"
    
        assert hasattr(mock_config, "experiment_name")
        assert len(mock_config.experiment_name) > 0

        mock_config_attributes = [item for item in dir(mock_config) if not item.startswith("_")]
        assert len(mock_config_attributes) == 12
        pass




    #@unittest.skip("for dev.")
    def test_override_parameters_with_dict(self):
        mock_args = self._mock_train_argument()
        mock_config = Test_Interface.mock_config_dict.copy()

        mlpylib.setup(mock_args)
        mlpylib.override_parameters(mock_config)

        assert mock_config["EPOCHS"] == 80
        assert mock_config["MODEL_TYPE"] == "crack"
        pass


    #@unittest.skip("for dev.")
    def test_override_parameters_insert_new_with_dict(self):
        mock_args = self._mock_train_argument()
        mock_config = Test_Interface.mock_config_dict.copy()

        mlpylib.setup(mock_args)
        mlpylib.override_parameters(mock_config, True)

        assert mock_config["EPOCHS"] == 80
        assert mock_config["MODEL_TYPE"] == "crack"
    
        assert "experiment_name" in mock_config
        assert len(mock_config["experiment_name"]) > 0

        assert len(mock_config) == 12
        pass



    #@unittest.skip("for dev.")
    def test_get_mlrun_parameter(self):
        mock_args = self._mock_train_argument()

        mlpylib.setup(mock_args)

        print(mlpylib.mlrun_parameters[mlpylib.MLRUN_PARAM_MLFLOW.MLFlowUri])

        assert len(mlpylib.mlrun_parameters[mlpylib.MLRUN_PARAM_MLFLOW.MLFlowUri]) > 0
        assert len(mlpylib.mlrun_parameters[mlpylib.MLRUN_PARAM_TRAIN.CodeGit]) > 0

        for item in mlpylib.MLRUN_PARAM_TRAIN:
            assert item in mlpylib.mlrun_parameters 
                
        pass




if __name__ == "__main__":
    unittest.main()