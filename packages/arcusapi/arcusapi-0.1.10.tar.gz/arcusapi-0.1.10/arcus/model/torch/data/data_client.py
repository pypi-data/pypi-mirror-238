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


import logging

import torch

from arcus.api_client import ArcusResponse
from arcus.constants import ARCUS_MODULE_NAME
from arcus.model.shared.data.data_client import (
    VerticalExternalDataClient as BaseVerticalExternalDataClient,
)
from arcus.model.torch.data.join_keys import JoinKeys
from arcus.model.torch.data.tensor import ExternalDataTensor

logger = logging.getLogger(ARCUS_MODULE_NAME)


class VerticalExternalDataClient(BaseVerticalExternalDataClient):
    def _fetch_external_data(
        self,
        internal_join_keys: JoinKeys,
    ) -> ExternalDataTensor:
        response: ArcusResponse = self.api_client.request(
            "POST",
            "model/data/features",
            params={
                "project_id": self.config.get_project_id(),
                "candidate_id": self.candidate_id,
            },
            json={"join_keys": internal_join_keys.to_json()},
        )

        if not response.status_ok:
            raise Exception("Unable to fetch external data from Arcus.")

        external_data_tensor: torch.Tensor = torch.tensor(
            response.data["data"], dtype=torch.float32
        )

        logger.debug(
            f"Fetched external data with shape {external_data_tensor.shape}."
        )

        assert (
            len(external_data_tensor.shape) == 2
        ), "External data must be 2-dimensional."

        assert self.external_data_dim == (
            external_data_tensor.shape[1]
            - len(self.external_join_column_indices)
        ), (
            "External data must have the same number of "
            + "dimensions as the model expects. "
            + f"Expected {self.external_data_dim}, got "
            + str(
                external_data_tensor.shape[1]
                - len(self.external_join_column_indices)
            )
            + "."
        )
        return ExternalDataTensor(external_data_tensor, self.feature_type)

    @property
    def shape(self) -> torch.Size:
        return torch.Size([len(self), self.external_data_dim])
