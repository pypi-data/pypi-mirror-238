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


from typing import List

from arcus.model.shared.config import Config
from arcus.model.shared.data.candidate_metadata import CandidateMetadata
from arcus.model.shared.data.external_feature_type import ExternalFeatureType
from arcus.model.shared.join_keys import JoinKeyMetadata


class ProjectCandidateMetadata:
    def __init__(
        self,
        config: Config,
        candidate_metadata: CandidateMetadata,
    ):
        """
        ProjectCandidateMetadata encapsulates both the project metadata and
        the candidate metadata. This is used to identify the external data
        and its type, as well as the project it belongs to and basic
        authentication information.
        """
        self.config = config
        self.candidate_metadata = candidate_metadata

        assertion_message = (
            "Candidate must have the same number of join columns "
            + "as the first-party data's join columns."
            + f" Candidate: {self.candidate_metadata.get_join_column_indices()}"
            + f" First-party: {self.config.get_join_column_indices()}"
        )

        if candidate_metadata.is_external():
            assert len(
                self.candidate_metadata.get_join_column_indices()
            ) == len(self.config.get_join_column_indices()), assertion_message

    def is_external(self) -> bool:
        return self.candidate_metadata.is_external()

    def get_candidate_id(self) -> str:
        return self.candidate_metadata.get_candidate_id()

    def get_data_dim(self) -> int:
        return self.candidate_metadata.get_data_dim()

    def get_feature_type(self) -> ExternalFeatureType:
        return self.candidate_metadata.get_feature_type()

    def get_api_key(self) -> str:
        return self.config.get_api_key()

    def get_project_id(self) -> str:
        return self.config.get_project_id()

    def get_config(self) -> Config:
        return self.config

    def get_external_join_column_indices(self) -> List[int]:
        return self.candidate_metadata.get_join_column_indices()

    def get_internal_join_key_metadata(self) -> JoinKeyMetadata:
        return self.config.get_join_key_metadata()
