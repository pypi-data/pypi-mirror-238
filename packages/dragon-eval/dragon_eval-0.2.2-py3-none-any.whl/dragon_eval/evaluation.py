#  Copyright 2022 Diagnostic Image Analysis Group, Radboudumc, Nijmegen, The Netherlands
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, Optional

import numpy as np
import pandas as pd
import seqeval.metrics
from evalutils.evalutils import (DEFAULT_EVALUATION_OUTPUT_FILE_PATH,
                                 DEFAULT_GROUND_TRUTH_PATH, DEFAULT_INPUT_PATH,
                                 ClassificationEvaluation)
from evalutils.io import FileLoader
from evalutils.validators import ExpectedColumnNamesValidator
from sklearn.metrics import cohen_kappa_score, roc_auc_score


class EvalType(Enum):
    """Problem type of the task"""
    NER = "named_entity_recognition"
    REGRESSION = "regression"
    BINARY_CLASSIFICATION = "binary classification"
    ORDINAL_MULTI_CLASS_CLASSIFICATION = "ordinal multi-class classification"
    NONORDINAL_MULTI_CLASS_CLASSIFICATION = "non-ordinal multi-class classification"

TASK_TYPE = {
    "Task000_Example_clf": EvalType.ORDINAL_MULTI_CLASS_CLASSIFICATION,
    "Task001_Example_reg": EvalType.REGRESSION,
    "Task002_Example_multi_reg": EvalType.REGRESSION,
    "Task003_Example_mednli": EvalType.ORDINAL_MULTI_CLASS_CLASSIFICATION,
    "Task004_Example_ner": EvalType.NER,
    "Task005_Example_multi_clf": EvalType.NONORDINAL_MULTI_CLASS_CLASSIFICATION,
    "Task006_Example_binary_clf": EvalType.BINARY_CLASSIFICATION,
    "Task007_Example_multi_binary_clf": EvalType.BINARY_CLASSIFICATION,
    "Task008_Example_multi_ner": EvalType.BINARY_CLASSIFICATION,
    "Task100_adhesion_clf": EvalType.BINARY_CLASSIFICATION,
    "Task101_anonymisation_ner": EvalType.NER,
    "Task102_colon_pathology_clf": EvalType.BINARY_CLASSIFICATION,
    "Task103_hip_clf": EvalType.NONORDINAL_MULTI_CLASS_CLASSIFICATION,
    "Task104_kidney_clf": EvalType.BINARY_CLASSIFICATION,
    "Task105_medical_terminology_ner": EvalType.NER,
    "Task106_nodules_clf": EvalType.BINARY_CLASSIFICATION,
    "Task107_nodules_diameter_clf": EvalType.BINARY_CLASSIFICATION,
    "Task108_nodules_diameter_reg": EvalType.REGRESSION,
    "Task112_pathology_tumor_origin_clf": EvalType.BINARY_CLASSIFICATION,
    "Task113_pathology_tissue_modality_clf": EvalType.NONORDINAL_MULTI_CLASS_CLASSIFICATION,
    "Task114_pathology_tissue_type_clf": EvalType.NONORDINAL_MULTI_CLASS_CLASSIFICATION,
    "Task117_prostate_pathology_clf": EvalType.ORDINAL_MULTI_CLASS_CLASSIFICATION,
    "Task118_prostate_radiology_clf": EvalType.ORDINAL_MULTI_CLASS_CLASSIFICATION,
    "Task119_prostate_radiology_prostate_volume_reg": EvalType.REGRESSION,
    "Task120_prostate_radiology_psa_reg": EvalType.REGRESSION,
    "Task121_prostate_radiology_psad_reg": EvalType.REGRESSION,
    "Task122_recist_baseline_followup_clf": EvalType.BINARY_CLASSIFICATION,
    "Task123_recist_lesion_size_clf": EvalType.BINARY_CLASSIFICATION,
    "Task124_recist_lesion_size_reg": EvalType.REGRESSION,
    "Task125_textual_entailment_clf": EvalType.ORDINAL_MULTI_CLASS_CLASSIFICATION,
}


class JSONLoader(FileLoader):
    """
    Custom file loader for JSON files.
    """

    def load(self, fname: Path) -> pd.DataFrame:
        if fname.is_dir():
            # skip directories
            return None

        with open(fname) as fp:
            return pd.read_json(fp, dtype={"uid": str})


def score_rsmape(
    *, y_true, y_pred, epsilon: float, ignore_missing_targets: bool = False,
):
    """Robust symmetric mean absolute percentage score (R-SMAPE)
    The R-SMAPE is a robust version of the symmetric mean absolute percentage error (SMAPE) by adding epsilon to the denominator.
    SMAPE is a symmetric version of the mean absolute percentage error (MAPE) by adding the absolute value of the predicted values to the denominator.
    This results in a score that is more robust to outliers and makes sure that swapping the true and predicted values does not change the score.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    # flatten arrays and maybe ignore missing targets
    if ignore_missing_targets:
        mask = ~np.isnan(y_true)
        y_true = y_true[mask]
        y_pred = y_pred[mask]
    else:
        y_pred = np.ravel(y_pred)
        y_true = np.ravel(y_true)

    # compute R-SMAPE
    numerator = np.abs(y_true - y_pred)
    denominator = np.abs(y_true) + np.abs(y_pred) + epsilon
    rsmape = numerator / denominator
    return 1 - np.mean(rsmape)


class DragonEval(ClassificationEvaluation):
    def __init__(self, folds: Iterable[int] = range(5), tasks: Optional[Iterable[str]] = None, **kwargs):
        super().__init__(
            file_loader=JSONLoader(),
            validators=(
                ExpectedColumnNamesValidator(
                    expected=("uid", ), extra_cols_check=False,
                ),
            ),
            join_key="uid",
            **kwargs,
        )
        self._scores: Dict[str, float] = {}
        self.folds = folds
        self.tasks = tasks

        if self.tasks is None:
            # get all tasks
            self.tasks = sorted([
                path.stem
                for path in self._ground_truth_path.glob(f"*.json")
            ])
            if not self.tasks:
                raise ValueError("Could not find any tasks!")
        else:
            # check if all tasks exist
            task_names = []
            for task in self.tasks:
                files_found = [path.stem for path in self._ground_truth_path.glob(f"*{task}*.json")]
                if not files_found:
                    raise ValueError(f"Could not find task: {task}")
                if len(files_found) > 1:
                    raise ValueError(f"Found multiple tasks matching {task}: {files_found}")
                task_names.append(files_found[0])
            if len(set(task_names)) != len(self.tasks):
                raise ValueError(f"Duplicate tasks found: {task_names}")
            self.tasks = task_names

        print(f"Evaluating {len(self.tasks)} tasks: {self.tasks}")

    def evaluate(self):
        for task_name in self.tasks:
            for fold in self.folds:
                job_name = f"{task_name}-fold{fold}"
                self.load(task_name=task_name, job_name=job_name)
                self.validate()
                self.merge_ground_truth_and_predictions()
                self.cross_validate()
                self.score(task_name=task_name, job_name=job_name)
        self.aggregate_scores()
        self.save()

    def load(self, *, task_name: str, job_name: str):
        """Loads ground truth and predictions for a given job name"""
        self._ground_truth_cases = self._file_loader.load(
            self._ground_truth_path / f"{task_name}.json"
        )
        self._predictions_cases = self._file_loader.load(
            self._predictions_path / job_name / "nlp-test-predictions.json"
        )

    def score(self, *, task_name: str, job_name: str):
        """Scores the predictions for a given task / job

        Args:
            task_name: Name of the task
            job_name: Name of the job (task_name-foldX)
        """
        print(f"Evaluating {job_name}")
        # select ground truth and prediction columns
        label_column = [col for col in self._cases.columns if col.endswith("_target")][0]
        prediction_column = label_column.replace("_target", "")
        if not prediction_column in self._cases.columns:
            raise ValueError(f"Could not find prediction column for {label_column} (job: {job_name})")

        y_true = self._cases[label_column]
        y_pred = self._cases[prediction_column]

        if TASK_TYPE[task_name] == EvalType.ORDINAL_MULTI_CLASS_CLASSIFICATION:
            # evaluate ordinal multi-class classification tasks
            # metric: Linear-weighted Cohen's kappa
            score = cohen_kappa_score(
                y1=y_true,
                y2=y_pred,
                weights="linear",
            )

        elif TASK_TYPE[task_name] == EvalType.NONORDINAL_MULTI_CLASS_CLASSIFICATION:
            # evaluate non-ordinal (multi-class) classification tasks
            # note: each subtask is the same, so we pool the labels and predictions
            #       (this is not actually true for the example task, but it is for the real tasks)
            # metric: Unweighted Cohen's kappa
            score = cohen_kappa_score(
                y1=y_true.explode(),
                y2=y_pred.explode(),
                weights=None,
            )

        elif TASK_TYPE[task_name] == EvalType.BINARY_CLASSIFICATION:
            # evaluate (multi-label) binary classification tasks
            # note: each subtask is the same, so we pool the labels and predictions
            # metric: AUC
            score = roc_auc_score(
                y_true=y_true.explode().explode().values.astype(int),
                y_score=y_pred.explode().explode().values.astype(float),
            )

        elif TASK_TYPE[task_name] == EvalType.REGRESSION:
            # evaluate regression tasks
            # note: for the multi-label regression task, each subtask is the same,
            #       so we pool the labels and predictions
            # metric: R-SMAPE
            epsilon = {
                "Task001_Example_reg": 4,
                "Task002_Example_multi_reg": 4,
                "Task115_prostate_radiology_prostate_volume_reg": 4,
                "Task116_prostate_radiology_psa_reg": 0.4,
                "Task117_prostate_radiology_psad_reg": 0.04,
                "Task120_nodules_diameter_reg": 4,
                "Task123_recist_lesion_size_reg": 4,
            }[task_name]

            score = score_rsmape(
                y_true=y_true.explode().astype(float),
                y_pred=y_pred.explode().astype(float),
                epsilon=epsilon,
                ignore_missing_targets=True,
            )

        elif TASK_TYPE[task_name] == EvalType.NER:
            # evaluate named entity recognition tasks
            # metric: F1 score
            score = seqeval.metrics.f1_score(
                y_true=y_true,
                y_pred=y_pred,
            )

        else:
            raise ValueError(f"Unexpexted task: {task_name}")

        # save score for the current job
        if task_name not in self._scores:
            self._scores[task_name] = {}
        self._scores[task_name][job_name] = score

    @property
    def _metrics(self) -> Dict:
        """Returns the calculated case and aggregate results"""
        return {
            "case": self._scores,
            "aggregates": self._aggregate_results,
        }

    @staticmethod
    def calculate_aggregate_results(scores):
        """Calculates the mean and std of the scores"""
        # calculate mean and std for each task
        aggregate_results = {}
        for task_name, scores in scores.items():
            aggregate_results[task_name] = {
                "mean": np.mean(list(scores.values())),
                "std": np.std(list(scores.values())),
            }

        return aggregate_results

    def aggregate_scores(self):
        """Aggregates the scores"""
        # calculate mean and std for each task
        self._aggregate_results = self.calculate_aggregate_results(self._scores)
    
        # calculate overall score
        self._aggregate_results["overall"] = {
            "mean": np.mean([score["mean"] for score in self._aggregate_results.values()]),
            "std": np.mean([score["std"] for score in self._aggregate_results.values()]),
        }

        print(f"Aggregate results:")
        for task_name, scores in self._aggregate_results.items():
            print(f"  {task_name}: {scores['mean']:.3f} ± {scores['std']:.3f}")


if __name__ == "__main__":
    DragonEval(
        ground_truth_path=DEFAULT_GROUND_TRUTH_PATH if DEFAULT_GROUND_TRUTH_PATH.exists() else Path("ground-truth"),
        predictions_path=DEFAULT_INPUT_PATH if DEFAULT_INPUT_PATH.exists() else Path("test-predictions"),
        output_file=DEFAULT_EVALUATION_OUTPUT_FILE_PATH if DEFAULT_EVALUATION_OUTPUT_FILE_PATH.parent.exists() else Path("test-output/metrics.json"),
    ).evaluate()
