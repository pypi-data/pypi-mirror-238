import json
import os
import unittest
import mlpylib
from mlpylib._util.nomenclature import (
    compute_experiment_name,
    compute_model_artifact_full_path,
    compute_model_artifact_name,
    compute_model_version_name,
    explain_model_artifact_name,
    is_verify_experiment,
    the_paramkey_run_id,
    the_paramkey_run_name,
    the_paramkey_run_name_pattern,
    the_paramkey_run_state
    )


class Test_Nomenclature(unittest.TestCase):

    def _mock_train_argument(self):
        with open(os.path.join(os.path.dirname(__file__), "mock-train-args.txt"), "r") as f:
            args = json.load(f)

        return ["--OVERRIDE_PARAMS", json.dumps(args)] 


    def test_explain_experiment_name(self):
        (environment, project_name, model_type) = mlpylib.explain_experiment_name("prod_WSD.ML.Raleigh.Bsir_crack")

        assert environment == "prod"
        assert project_name == "WSD.ML.Raleigh.Bsir"
        assert model_type == "crack"

        pass



    def test_explain_experiment_name(self):
        mock_args = self._mock_train_argument()

        mlpylib.setup(mock_args)
        (environment, project_name, model_type) = mlpylib.explain_experiment_name()

        assert environment == "prod"
        assert project_name == "WSD.ML.Sample.Bsir"
        assert model_type == "crack"

        pass



    def test_compute_model_artifact_full_path(self):
        model_artifact_name = compute_model_artifact_full_path("prod_WSD.ML.Raleigh.Bsir_verify", "crack", True)
        assert model_artifact_name == "model/WSD.ML.Raleigh.Bsir_crack"

        model_artifact_name = compute_model_artifact_full_path("prod_WSD.ML.Raleigh.Bsir_verify", "grind", False)
        assert model_artifact_name == "reusemodel/WSD.ML.Raleigh.Bsir_grind"

        pass



    def test_compute_model_artifact_name(self):
        model_artifact_name = compute_model_artifact_name("prod_WSD.ML.Raleigh.Bsir_verify", "crack")
        assert model_artifact_name == "WSD.ML.Raleigh.Bsir_crack"

        pass


    def test_explain_model_artifact_name(self):
        (project_name, model_type) = explain_model_artifact_name("WSD.ML.Raleigh.Bsir_crack")
        assert project_name == "WSD.ML.Raleigh.Bsir"
        assert model_type == "crack"

        (project_name, model_type) = explain_model_artifact_name("WSD.ML.Raleigh.Bsir_grind")
        assert project_name == "WSD.ML.Raleigh.Bsir"
        assert model_type == "grind"

        pass



    def test_compute_experiment_name(self):
        actual = compute_experiment_name("prod", "WSD.ML.Raleigh.Bsir", "crack")
        assert actual == "prod_WSD.ML.Raleigh.Bsir_crack"
        pass


    def test_compute_model_version_name(self):
        actual = compute_model_version_name("WSD.ML.Raleigh.Bsir", "crack")
        assert actual == "WSD.ML.Raleigh.Bsir_crack"        

        actual = compute_model_version_name("WSD.ML.Raleigh.Bsir", "grind")
        assert actual == "WSD.ML.Raleigh.Bsir_grind"        
        pass


    def test_is_verify_experiment(self):
        actual = is_verify_experiment("prod_WSD.ML.Raleigh.Bsir_crack")
        assert actual == False

        actual = is_verify_experiment("prod_WSD.ML.Raleigh.Bsir_grind")
        assert actual == False

        actual = is_verify_experiment("prod_WSD.ML.Raleigh.Bsir_verify")
        assert actual == True
        pass


    def test_the_paramkey_run_id(self):
        actual = the_paramkey_run_id("crack")
        assert actual == "ml.crack_runid"

        actual = the_paramkey_run_id("grind")
        assert actual == "ml.grind_runid"

        pass


    def test_the_paramkey_run_name(self):
        actual = the_paramkey_run_name("crack")
        assert actual == "ml.crack_run"

        actual = the_paramkey_run_name("grind")
        assert actual == "ml.grind_run"

        pass


    def test_the_paramkey_run_name_pattern(self):
        actual = the_paramkey_run_name_pattern()
        assert actual.match("ml.crack_run") is not None
        assert actual.match("ml.grind_run") is not None

        assert actual.match("ml.grind_runid") is None
        assert actual.match("ml.grind_state") is None
        assert actual.match("ml.git_code") is None
        assert actual.match("xml.crack_run") is None

        pass


    def test_the_paramkey_run_state(self):
        actual = the_paramkey_run_state("crack")
        assert actual == "ml.crack_state"

        actual = the_paramkey_run_state("grind")
        assert actual == "ml.grind_state"

        pass

    pass



if __name__ == "__main__":
    unittest.main()