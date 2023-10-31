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


import torch

from arcus.model.shared.data.array import ExternalDataArray


class ExternalDataTensor(ExternalDataArray):
    pass


class VerticallyAugmentedTensor:
    """
    Represents a tensor that is vertically augmented with external data
        from the Arcus Data Platform.
    Args:
        first_party_data: The first party data.
        external_data: The external data.
    """

    def __init__(
        self,
        first_party_data: torch.Tensor,
        external_data: ExternalDataTensor,
    ):
        assert len(first_party_data) == len(
            external_data
        ), "Internal and external data must have the same number of samples."

        self.first_party_data = first_party_data
        self.external_data = external_data

    def __len__(self) -> int:
        return len(self.first_party_data)

    def get_first_party_data(self) -> torch.Tensor:
        return self.first_party_data

    def get_external_data(self) -> ExternalDataTensor:
        return self.external_data
