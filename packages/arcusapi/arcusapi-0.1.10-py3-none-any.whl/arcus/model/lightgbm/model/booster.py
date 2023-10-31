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


from typing import List, Union

import lightgbm as lgb
import numpy as np
import scipy.sparse
from lightgbm.basic import _LGBM_PredictDataType

from arcus.model.shared.data.project_candidate_metadata import (
    ProjectCandidateMetadata,
)


class Booster(lgb.Booster):
    def __init__(
        self,
        underlying_booster: lgb.Booster,
        project_candidate_metadata: ProjectCandidateMetadata,
    ):
        self.project_candidate_metadata = project_candidate_metadata
        self.underlying_booster = underlying_booster

    def __del__(self):
        pass

    # Keep all existing methods of self.underlying_booster except those
    # overriden here.
    def __getattr__(self, attr):
        print(f"__getattr__ called with {attr}")
        if hasattr(self.underlying_booster, attr):
            attr_requested = getattr(self.underlying_booster, attr)
            print(f"Returning {attr_requested}")
            return attr_requested

        raise AttributeError(f"Attribute {attr} not found.")

    # Many internal methods of Booster will set attributes directly, so we
    # need to override __setattr__ to make sure that we set the attributes
    # on the underlying booster instead of on this object.
    def __setattr__(self, name, value):
        if "underlying_booster" in self.__dict__:
            setattr(self.underlying_booster, name, value)
        else:
            super().__setattr__(name, value)

    def predict(
        self,
        data: _LGBM_PredictDataType,
        start_iteration: int = 0,
        num_iteration: int = -1,
        raw_score: bool = False,
        pred_leaf: bool = False,
        pred_contrib: bool = False,
        data_has_header: bool = False,
        validate_features: bool = False,
    ) -> Union[np.ndarray, scipy.sparse.spmatrix, List[scipy.sparse.spmatrix]]:
        # TODO (CLI-145): Make predictions use the project candidate metadata
        # to use external data to enrich predictions.
        raise NotImplementedError


class CVBooster(lgb.CVBooster):
    def __init__(
        self,
        underlying_cvbooster: lgb.CVBooster,
        project_candidate_metadata: ProjectCandidateMetadata,
    ):
        self.project_candidate_metadata = project_candidate_metadata
        self.underlying_cvbooster = underlying_cvbooster

        if hasattr(self.underlying_cvbooster, "boosters"):
            for i, booster in enumerate(self.underlying_cvbooster.boosters):
                self.underlying_cvbooster.boosters[i] = Booster(
                    booster, project_candidate_metadata
                )

    # Keep all existing methods of self.underlying_cvbooster except those
    # overriden here.
    def __getattr__(self, attr):
        if hasattr(self.underlying_cvbooster, attr):
            return getattr(self.underlying_cvbooster, attr)

        raise AttributeError(f"Attribute {attr} not found.")

    # Many internal methods of CVBooster will set attributes directly, so we
    # need to override __setattr__ to make sure that we set the attributes
    # on the underlying cvbooster instead of on this object.
    def __setattr__(self, name, value):
        if "underlying_cvbooster" in self.__dict__:
            setattr(self.underlying_cvbooster, name, value)
        else:
            super().__setattr__(name, value)
