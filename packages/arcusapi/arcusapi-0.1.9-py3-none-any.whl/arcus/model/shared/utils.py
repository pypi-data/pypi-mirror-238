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
from typing import Optional

from arcus.api_client import APIClient, ArcusResponse
from arcus.constants import ARCUS_MODULE_NAME
from arcus.model.shared.config import Config
from arcus.model.shared.data.candidate_metadata import CandidateMetadata
from arcus.model.shared.data.external_feature_type import ExternalFeatureType
from arcus.model.shared.data.project_candidate_metadata import (
    ProjectCandidateMetadata,
)

logger = logging.getLogger(ARCUS_MODULE_NAME)


def get_selection_metadata(
    config: Config,
) -> Optional[ProjectCandidateMetadata]:
    """
    Gets the Arcus metadata of the selction for the given model using the
    Arcus API.
    """
    api_client = APIClient(config)

    response: ArcusResponse = api_client.request(
        "GET",
        "model/selections/metadata",
        params={"project_id": config.get_project_id()},
    )

    if not response.status_ok:
        raise RuntimeError(
            "Failed to retrieve data selection. Make sure a selection has "
            + "been made for this project."
        )
        return None

    response_data = response.data

    candidate_metadata = CandidateMetadata(
        candidate_id=response_data["candidate_id"],
        data_dim=response_data["data_dim"],
        join_column_indices=response_data["join_column_indices"],
        feature_type=ExternalFeatureType(response_data["feature_type"]),
        is_external=response_data["is_external"],
    )

    logger.debug(f"Retrieved selection metadata: {candidate_metadata}")

    return ProjectCandidateMetadata(
        config=config,
        candidate_metadata=candidate_metadata,
    )
