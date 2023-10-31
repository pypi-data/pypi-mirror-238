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


from typing import List, Optional

from lightgbm.callback import CallbackEnv, EarlyStopException

from arcus.model.shared.config import Config
from arcus.model.shared.data.candidate_metadata import CandidateMetadata
from arcus.model.shared.metrics import (
    SUPPORTED_METRICS,
    MetricStore,
    Stage,
    StepMetrics,
)


class MetricsCallback:
    def __init__(
        self,
        config: Config,
        candidate_metadata: CandidateMetadata,
        stage: Stage,
    ):
        self.metric_store = None
        self.config = config
        self.candidate_metadata = candidate_metadata
        self.stage = stage

    def _init(self, env: CallbackEnv):
        metric_names = list(
            {m[1] for m in env.evaluation_result_list}.intersection(
                set(SUPPORTED_METRICS)
            )
        )

        self.metric_store = MetricStore(
            self.config,
            self.candidate_metadata,
            metric_names,
            self.stage,
        )

    def __call__(self, env: CallbackEnv):
        if self.metric_store is None:
            self._init(env)

        metrics_dict = {
            evaluation_result[1]: evaluation_result[2]
            for evaluation_result in env.evaluation_result_list
        }

        # TODO (CLI-145): During cross-validation, the same metrics callback
        # object is used for all folds. This means that the metric store is
        # used against multiple folds, rather than as a sequential list
        # per iteration. Instead, our metric store should be able to average
        # across folds, e.g. we may want to provide the iteration number
        # along with the metrics.
        should_stop = self.metric_store.log(metrics_dict)

        if should_stop:
            raise EarlyStopException(env.iteration, env.evaluation_result_list)

    def get_metrics(self) -> Optional[List[StepMetrics]]:
        if self.metric_store is None:
            return None
        return self.metric_store.get()

    def post_metrics(self) -> None:
        if self.metric_store is None:
            return None
        self.metric_store.post_metrics()
