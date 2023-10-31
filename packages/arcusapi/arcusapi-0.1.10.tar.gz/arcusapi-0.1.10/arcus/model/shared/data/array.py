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


from typing import List, Optional, Union

import numpy as np

from arcus.model.shared.data.external_feature_type import ExternalFeatureType

try:
    import torch

    ARRAY_TYPE = Union[np.ndarray, torch.Tensor]
except ImportError:
    ARRAY_TYPE = np.ndarray


class ExternalDataArray:
    """
    Represents an array that is obtained from the Arcus data platform.
    Args:
        external_data_values: The values of the data that is obtained from
            the Arcus data platform.
        feature_type: The type of the external data (raw or embeddings).
    """

    def __init__(
        self,
        external_data_values: ARRAY_TYPE,
        feature_type: Optional[ExternalFeatureType] = ExternalFeatureType.RAW,
    ):
        """
        Represents a tensor that is obtained from the Arcus data platform.
        """
        self.external_data_values = external_data_values
        self.feature_type = feature_type

    def __len__(self):
        return len(self.external_data_values)

    @property
    def shape(self):
        return self.external_data_values.shape

    def __getitem__(self, index: Union[int, List[int], slice, ARRAY_TYPE]):
        return ExternalDataArray(
            self.external_data_values[index],
            self.feature_type,
        )

    def is_raw(self) -> bool:
        return self.feature_type is ExternalFeatureType.RAW

    def is_embedding(self) -> bool:
        return self.feature_type is ExternalFeatureType.EMBEDDING

    def get_data(self) -> np.ndarray:
        return self.external_data_values
