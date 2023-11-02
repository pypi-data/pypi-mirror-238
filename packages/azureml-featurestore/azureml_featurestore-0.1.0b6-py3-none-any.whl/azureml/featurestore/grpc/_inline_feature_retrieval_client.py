# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import List

from azureml.featurestore.contracts.feature import Feature
from azureml.featurestore.online import OnlineFeatureGetter

from azure.identity import DefaultAzureCredential


class InlineFeatureRetrievalClient:
    def get_online_features(self, features: List[Feature], observation_df: "pandas.DataFrame", **kwargs):
        feature_uris = [feature.uri for feature in features]
        online_feature_getter = OnlineFeatureGetter(DefaultAzureCredential())
        return online_feature_getter.get_online_features(feature_uris, observation_df)

    def get_offline_features(
        self, features: List[Feature], observation_df: "pyspark.sql.DataFrame", timestamp_column: str
    ):
        raise NotImplementedError()
