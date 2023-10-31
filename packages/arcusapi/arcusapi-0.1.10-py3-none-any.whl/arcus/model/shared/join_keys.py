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


from typing import Dict, List

import numpy as np


class JoinKeyMetadata:
    def __init__(self, column_indices: List[int], column_headers: List[str]):
        assert len(column_indices) == len(
            column_headers
        ), "Number of column indices must match number of column headers."
        self.column_indices = column_indices
        self.column_headers = column_headers

    def get_column_indices(self) -> List[int]:
        return self.column_indices

    def get_column_headers(self) -> List[str]:
        return self.column_headers


def intersecting_row_indices(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Returns which rows of y are present in x.
    """
    x_rows = set(tuple(row) for row in x)

    intersecting_rows = []
    for i, row in enumerate(y):
        if tuple(row) in x_rows:
            intersecting_rows.append(i)

    return np.array(intersecting_rows)


class JoinKeys:
    def __init__(self, keys: np.ndarray, key_metadata: JoinKeyMetadata):
        """
        JoinKeys are a 2D array of keys that are used to join two datasets.
        The first dimension is the batch dimension, and the second
        dimension is the number of keys. The keys are assumed to be unique.
        """
        self.keys = keys
        self.key_metadata = key_metadata

    def __getitem__(self, index: int) -> np.ndarray:
        return self.keys[index]

    def __len__(self):
        return len(self.keys)

    def get_keys(self) -> np.ndarray:
        return self.keys

    def to_json(self) -> Dict[str, List]:
        join_column_headers = self.key_metadata.get_column_headers()
        return {
            join_column_headers[i]: self.keys[:, i].tolist()
            for i in range(len(join_column_headers))
        }

    def intersecting_indices(self, other) -> np.ndarray:
        intersecting_rows = intersecting_row_indices(self.keys, other.keys)

        assert len(intersecting_rows) == len(
            self.keys
        ), "Missing keys when attempting to join keys."

        return intersecting_rows

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, JoinKeys):
            return False
        return np.array_equal(self.get_keys(), __value.get_keys())
