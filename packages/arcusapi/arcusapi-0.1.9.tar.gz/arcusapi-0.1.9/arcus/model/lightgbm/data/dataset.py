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


import lightgbm as lgb
import pandas as pd
from lightgbm.compat import DATATABLE_INSTALLED, dt_DataTable

from arcus.model.shared.data.data_client import VerticalExternalDataClient
from arcus.model.shared.join_keys import JoinKeyMetadata, JoinKeys


class Dataset(lgb.Dataset):
    def __init__(
        self,
        underyling_dataset: lgb.Dataset,
        external_data_client: VerticalExternalDataClient,
        internal_join_key_metadata: JoinKeyMetadata,
    ):
        self.external_data_client = external_data_client
        self.internal_join_key_metadata = internal_join_key_metadata
        self.join_column_indices = (
            internal_join_key_metadata.get_column_indices()
        )
        self.free_raw_first_party_data = underyling_dataset.free_raw_data
        self.underyling_dataset = underyling_dataset

    # Keep all existing methods of self.underyling_dataset except those
    # overriden here.
    def __getattr__(self, attr):
        if hasattr(self.underyling_dataset, attr):
            return getattr(self.underyling_dataset, attr)

        raise AttributeError(f"Attribute {attr} not found.")

    # Many internal methods of Dataset will set attributes directly, so we
    # need to override __setattr__ to make sure that we set the attributes
    # on the underlying dataset instead of on this object.
    def __setattr__(self, name, value):
        if "underyling_dataset" in self.__dict__:
            setattr(self.underyling_dataset, name, value)
        else:
            super().__setattr__(name, value)

    def _get_internal_join_keys(self) -> JoinKeys:
        if self.underyling_dataset.get_data() is None:
            raise Exception("Dataset data is not initialized.")

        data = self.underyling_dataset.get_data()
        if DATATABLE_INSTALLED and isinstance(data, dt_DataTable):
            data = data.to_numpy()
        elif isinstance(data, pd.DataFrame):
            data = data.values

        internal_join_keys = JoinKeys(
            keys=data[:, self.join_column_indices],
            key_metadata=self.internal_join_key_metadata,
        )

        return internal_join_keys

    def construct(self) -> "Dataset":
        """
        construct() is called by LightGBM to build the dataset as a lazy
        initialization method. During this initialization, we can fetch
        data from Arcus and add it to the dataset.
        """
        # First, construct the underlying first party dataset. This should
        # set self.underyling_dataset.data. We prevent this from being freed
        # so we can retrieve the data to join with the external data.
        self.underyling_dataset.free_raw_data = False
        self.underyling_dataset.construct()

        internal_join_keys = self._get_internal_join_keys()

        # Next, we need to get the data from the external data client. We
        # represent this as a lightgbm.Dataset object from a numpy array.
        external_data_array = self.external_data_client.fetch_batch(
            internal_join_keys=internal_join_keys
        )
        external_data_dataset = lgb.Dataset(
            data=external_data_array, free_raw_data=False
        )
        external_data_dataset.construct()

        underlying_categorical_feature = (
            self.underyling_dataset.categorical_feature
        )
        underlying_pandas_categorical = (
            self.underyling_dataset.pandas_categorical
        )
        # We add the features from the external data to the underlying
        # dataset.
        self.underyling_dataset.add_features_from(external_data_dataset)

        # Update the categorical features to include the new features from
        # the external data. For now, assume external data does not have any
        # categorical features.
        self.set_categorical_feature(
            categorical_feature=underlying_categorical_feature
        )

        self.underyling_dataset.pandas_categorical = (
            underlying_pandas_categorical
        )

        # If the underyling dataset had been specified to free the raw data,
        # we can free the raw data now that we have added the external data.
        if self.free_raw_first_party_data:
            self.underyling_dataset.free_raw_data = True

        # Reconstruct the dataset now that we have added the external data and
        # updated the set of categorical features.
        self.underyling_dataset.construct()

        return self
