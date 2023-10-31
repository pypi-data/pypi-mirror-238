# Copyright [2023] [Arcus Inc.]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import copy
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

import numpy as np
from lightgbm.basic import Dataset as LightGBMDataset
from lightgbm.basic import (
    _LGBM_CategoricalFeatureConfiguration,
    _LGBM_EvalFunctionResultType,
    _LGBM_FeatureNameConfiguration,
)
from lightgbm.compat import _LGBMBaseCrossValidator
from lightgbm.engine import cv as lightgbm_cv
from lightgbm.engine import train as lightgbm_train

from arcus.model.lightgbm.callback import MetricsCallback
from arcus.model.lightgbm.data import Dataset
from arcus.model.lightgbm.model.booster import Booster, CVBooster
from arcus.model.shared.config import Config
from arcus.model.shared.data.data_client import VerticalExternalDataClient
from arcus.model.shared.data.project_candidate_metadata import (
    ProjectCandidateMetadata,
)
from arcus.model.shared.metrics import Stage
from arcus.model.shared.trial import Trial
from arcus.model.shared.utils import get_selection_metadata

_LGBM_CustomMetricFunction = Union[
    Callable[
        [np.ndarray, Dataset],
        _LGBM_EvalFunctionResultType,
    ],
    Callable[[np.ndarray, Dataset], List[_LGBM_EvalFunctionResultType]],
]

_LGBM_PreprocFunction = Callable[
    [Dataset, Dataset, Dict[str, Any]], Tuple[Dataset, Dataset, Dict[str, Any]]
]


def _wrap_dataset_with_arcus_metadata(
    dataset: LightGBMDataset,
    project_candidate_metadata: ProjectCandidateMetadata,
) -> LightGBMDataset:
    external_data_client = VerticalExternalDataClient(
        project_candidate_metadata=project_candidate_metadata,
    )

    internal_join_key_metadata = (
        project_candidate_metadata.get_internal_join_key_metadata()
    )
    return Dataset(
        underlying_dataset=dataset,
        external_data_client=external_data_client,
        internal_join_key_metadata=internal_join_key_metadata,
    )


def _cv_common(
    params: Dict[str, Any],
    train_set: LightGBMDataset,
    num_boost_round: int = 100,
    folds: Optional[
        Union[Iterable[Tuple[np.ndarray, np.ndarray]], _LGBMBaseCrossValidator]
    ] = None,
    nfold: int = 5,
    stratified: bool = True,
    shuffle: bool = True,
    metrics: Optional[Union[str, List[str]]] = None,
    feval: Optional[
        Union[_LGBM_CustomMetricFunction, List[_LGBM_CustomMetricFunction]]
    ] = None,
    init_model: Optional[Union[str, Path, Booster]] = None,
    feature_name: _LGBM_FeatureNameConfiguration = "auto",
    categorical_feature: _LGBM_CategoricalFeatureConfiguration = "auto",
    fpreproc: Optional[_LGBM_PreprocFunction] = None,
    seed: int = 0,
    callbacks: Optional[List[Callable]] = None,
    eval_train_metric: bool = False,
    return_cvbooster: bool = False,
    project_candidate_metadata: Optional[ProjectCandidateMetadata] = None,
) -> Dict[str, Union[List[float], CVBooster]]:
    if (
        project_candidate_metadata is None
        or not project_candidate_metadata.is_external()
    ):
        return lightgbm_cv(
            params,
            train_set,
            num_boost_round,
            folds,
            nfold,
            stratified,
            shuffle,
            metrics,
            feval,
            init_model,
            feature_name,
            categorical_feature,
            fpreproc,
            seed,
            callbacks,
            eval_train_metric,
            return_cvbooster,
        )

    train_set = _wrap_dataset_with_arcus_metadata(
        train_set,
        project_candidate_metadata,
    )

    return lightgbm_cv(
        params,
        train_set,
        num_boost_round,
        folds,
        nfold,
        stratified,
        shuffle,
        metrics,
        feval,
        init_model,
        feature_name,
        categorical_feature,
        fpreproc,
        seed,
        callbacks,
        eval_train_metric,
        return_cvbooster,
    )


def trial(
    config: Config,
    params: Dict[str, Any],
    train_set: LightGBMDataset,
    num_boost_round: int = 100,
    folds: Optional[
        Union[Iterable[Tuple[np.ndarray, np.ndarray]], _LGBMBaseCrossValidator]
    ] = None,
    nfold: int = 5,
    stratified: bool = True,
    shuffle: bool = True,
    metrics: Optional[Union[str, List[str]]] = None,
    feval: Optional[
        Union[_LGBM_CustomMetricFunction, List[_LGBM_CustomMetricFunction]]
    ] = None,
    init_model: Optional[Union[str, Path, Booster]] = None,
    feature_name: _LGBM_FeatureNameConfiguration = "auto",
    categorical_feature: _LGBM_CategoricalFeatureConfiguration = "auto",
    fpreproc: Optional[_LGBM_PreprocFunction] = None,
    seed: int = 0,
    callbacks: Optional[List[Callable]] = None,
    eval_train_metric: bool = False,
) -> Trial:
    if callbacks is None:
        callbacks = []

    trial = Trial(config)
    original_callbacks = callbacks

    for (
        candidate_id,
        candidate_metadata,
    ) in trial.get_candidates_dict().items():
        curr_metadata = ProjectCandidateMetadata(
            config=config,
            candidate_metadata=candidate_metadata,
        )

        trial_callbacks = copy.deepcopy(original_callbacks)
        reporting_callback = MetricsCallback(
            config, curr_metadata, Stage.TRIAL
        )
        trial_callbacks.append(reporting_callback)

        _cv_common(
            params,
            train_set,
            num_boost_round,
            folds,
            nfold,
            stratified,
            shuffle,
            metrics,
            feval,
            init_model,
            feature_name,
            categorical_feature,
            fpreproc,
            seed,
            callbacks=trial_callbacks,
            eval_train_metric=eval_train_metric,
            return_cvbooster=False,
            project_candidate_metadata=curr_metadata,
        )

        reporting_callback.post_metrics()

        trial.store_candidate_metrics(
            candidate_id=candidate_id,
            metrics=reporting_callback.get_metrics(),
        )

    trial.complete()
    return trial


def cv(
    config: Config,
    params: Dict[str, Any],
    train_set: LightGBMDataset,
    num_boost_round: int = 100,
    folds: Optional[
        Union[Iterable[Tuple[np.ndarray, np.ndarray]], _LGBMBaseCrossValidator]
    ] = None,
    nfold: int = 5,
    stratified: bool = True,
    shuffle: bool = True,
    metrics: Optional[Union[str, List[str]]] = None,
    feval: Optional[
        Union[_LGBM_CustomMetricFunction, List[_LGBM_CustomMetricFunction]]
    ] = None,
    init_model: Optional[Union[str, Path, Booster]] = None,
    feature_name: _LGBM_FeatureNameConfiguration = "auto",
    categorical_feature: _LGBM_CategoricalFeatureConfiguration = "auto",
    fpreproc: Optional[_LGBM_PreprocFunction] = None,
    seed: int = 0,
    callbacks: Optional[List[Callable]] = None,
    eval_train_metric: bool = False,
    return_cvbooster: bool = False,
) -> Dict[str, Union[List[float], CVBooster]]:
    selection_project_candidate_metadata = get_selection_metadata(config)
    if callbacks is None:
        callbacks = []

    reporting_callback = MetricsCallback(
        config,
        selection_project_candidate_metadata,
        Stage.FIT,
    )

    callbacks.append(reporting_callback)

    cv_results = _cv_common(
        params,
        train_set,
        num_boost_round,
        folds,
        nfold,
        stratified,
        shuffle,
        metrics,
        feval,
        init_model,
        feature_name,
        categorical_feature,
        fpreproc,
        seed,
        callbacks,
        eval_train_metric,
        return_cvbooster,
        project_candidate_metadata=selection_project_candidate_metadata,
    )

    if return_cvbooster:
        original_cv_booster = cv_results["cvbooster"]
        cv_results["cvbooster"] = CVBooster(
            original_cv_booster,
            selection_project_candidate_metadata,
        )

    return cv_results


def train(
    config: Config,
    params: Dict[str, Any],
    train_set: LightGBMDataset,
    num_boost_round: int = 100,
    valid_sets: Optional[List[LightGBMDataset]] = None,
    valid_names: Optional[List[str]] = None,
    feval: Optional[
        Union[_LGBM_CustomMetricFunction, List[_LGBM_CustomMetricFunction]]
    ] = None,
    init_model: Optional[Union[str, Path, Booster]] = None,
    feature_name: _LGBM_FeatureNameConfiguration = "auto",
    categorical_feature: _LGBM_CategoricalFeatureConfiguration = "auto",
    keep_training_booster: bool = False,
    callbacks: Optional[List[Callable]] = None,
) -> Booster:
    selection_project_candidate_metadata = get_selection_metadata(config)
    if callbacks is None:
        callbacks = []

    reporting_callback = MetricsCallback(
        config,
        selection_project_candidate_metadata,
        Stage.FIT,
    )

    callbacks.append(reporting_callback)

    train_set = _wrap_dataset_with_arcus_metadata(
        train_set,
        selection_project_candidate_metadata,
    )

    original_booster = lightgbm_train(
        params,
        train_set,
        num_boost_round,
        valid_sets,
        valid_names,
        feval,
        init_model,
        feature_name,
        categorical_feature,
        keep_training_booster,
        callbacks,
    )

    return Booster(
        original_booster,
        selection_project_candidate_metadata,
    )
