# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from datetime import datetime
from typing import Dict, Optional

from azureml.featurestore._feature_set import FeatureSet
from azureml.featurestore._utils._constants import (
    CREATE_TIMESTAMP_COLUMN,
    NUMBER_OF_OFFLINE_MATERIALIZED_ROWS,
    NUMBER_OF_ONLINE_MATERIALIZED_ROWS,
    NUMBER_OF_SOURCE_ROWS,
    PACKAGE_NAME,
    SYS_CREATE_TIMESTAMP_COLUMN,
    SYS_UPDATE_TIMESTAMP_COLUMN,
)
from azureml.featurestore._utils.spark_utils import _deduplicate_dataframe
from azureml.featurestore._utils.utils import _build_logger
from azureml.featurestore.online._online_feature_materialization import materialize_online

from azure.ai.ml._exception_helper import log_and_raise_error
from azure.ai.ml._telemetry.activity import ActivityType, monitor_with_activity
from azure.ai.ml.exceptions import MlException

package_logger = None


def _get_logger():
    global package_logger
    if package_logger is None:
        package_logger = _build_logger(__name__)
    return package_logger


@monitor_with_activity(_get_logger(), f"{PACKAGE_NAME}->Materialize", ActivityType.PUBLICAPI)
def materialize(
    *,
    feature_set: FeatureSet,
    feature_window_start_time: Optional[datetime] = None,
    feature_window_end_time: Optional[datetime] = None,
    upsert: bool = True,
    offline=False,
    online=False,
    bootstrap=False,
    **kwargs,
) -> Dict:
    """Materialize a feature set into offline store (if applicable)

    :param feature_set: the feature set to materialize
    :type feature_set: FeatureSet
    :param feature_window_start_time: feature window start time
    :type feature_window_start_time: datetime, optional
    :param feature_window_end_time: feature window end time
    :type feature_window_end_time: datetime, optional
    :param upsert(backward compatibilty): True: perform insert and update, false: perform append, default: True
    :type upsert: bool, optional
    :param offline(new): materialize source data into offline store, default: False
    :type offline(new): bool, optional
    :param online(new): materialize source data into online store, default: False
    :type online: bool, optional
    :param boostrap(new): materialize feature set data from offline store into online store, default: False
    :type boostrap: bool, optional

    Returns:
        Dict: metrics
    """
    try:
        if online or offline:
            offline_df = None
            source_df = None
            offline_prefix = kwargs.get("offline_prefix", None)
            online_prefix = kwargs.get("online_prefix", None)
            replace = kwargs.get("replace", True)
            number_of_online_materialized_rows = 0
            number_of_offline_materialized_rows = 0
            number_of_source_rows = 0

            if offline or not bootstrap:
                source_df = feature_set.to_spark_dataframe(
                    feature_window_start_date_time=feature_window_start_time,
                    feature_window_end_date_time=feature_window_end_time,
                    use_materialized_data=False,
                    dedup=False,
                )
                source_df.persist()

                # empty data sanity check
                if source_df:
                    number_of_source_rows = source_df.count()

                    join_keys = [index_col.name for e in feature_set.entities for index_col in e.index_columns]

                    # deduplicate data
                    source_df, has_dup = _deduplicate_dataframe(
                        df=source_df, join_keys=join_keys, timestamp_column=feature_set.source.timestamp_column.name
                    )

                    from pyspark.sql.functions import current_timestamp

                    cur_time = current_timestamp()

                    if feature_set.feature_transformation_code or CREATE_TIMESTAMP_COLUMN not in source_df.columns:
                        source_df = source_df.withColumn(CREATE_TIMESTAMP_COLUMN, cur_time)

                    source_df = source_df.withColumn(SYS_CREATE_TIMESTAMP_COLUMN, cur_time)
                    source_df = source_df.withColumn(SYS_UPDATE_TIMESTAMP_COLUMN, cur_time)
                else:
                    print("[Materialization Job] Source data is empty, please check feature source")

            if offline:
                print(
                    "[Materialization Job] Materializing feature set: {}, version: {} into offline store..".format(
                        feature_set.name, feature_set.version
                    )
                )
                number_of_offline_materialized_rows = feature_set.offline_store.write_data(
                    feature_set=feature_set,
                    df=source_df,
                    feature_window_start_time=feature_window_start_time,
                    feature_window_end_time=feature_window_end_time,
                    upsert=replace,
                    replace=replace,
                    materialization_version=offline_prefix,
                )
            if online:
                if bootstrap:
                    offline_df = feature_set.offline_store.read_data(
                        feature_set=feature_set,
                        feature_window_start_time=feature_window_start_time,
                        feature_window_end_time=feature_window_end_time,
                        materialization_version=offline_prefix,
                    )
                    if offline_df:
                        number_of_source_rows = offline_df.count()
                        print(
                            "[Materialization Job] Materializing feature set: {}, version: {} data from offline store into online store..".format(
                                feature_set.name, feature_set.version
                            )
                        )
                        number_of_online_materialized_rows = materialize_online(
                            feature_set=feature_set,
                            dataframe_to_store=offline_df,
                            materialization_version=online_prefix,
                        )
                    else:
                        print("[Materialization Job] Offline data is empty, please check offline store")
                elif source_df:
                    print(
                        "[Materialization Job] Materializing feature set: {}, version: {} from source into online store..".format(
                            feature_set.name, feature_set.version
                        )
                    )
                    number_of_online_materialized_rows = materialize_online(
                        feature_set=feature_set, dataframe_to_store=source_df, materialization_version=online_prefix
                    )
        else:
            # backward compatibility
            if not feature_set.offline_store and not feature_set.online_store:
                raise Exception(
                    f"Feature set {feature_set.name}, version{feature_set.version}'s doesn't belong to any offline or online store, please register it with a feature store with offline or online store"
                )

            if not feature_set.materialization_settings:
                raise Exception(
                    f"Feature set {feature_set.name}, version{feature_set.version}'s materialization settings is empty, please set materialization policy"
                )

            source_df = feature_set.to_spark_dataframe(
                feature_window_start_date_time=feature_window_start_time,
                feature_window_end_date_time=feature_window_end_time,
                use_materialized_data=False,
                dedup=False,
            )
            source_df.persist()

            # empty data sanity check
            number_of_source_rows = source_df.count()
            if number_of_source_rows == 0:
                print("[Materialization Job] Input data is empty, please check input data")
                return {NUMBER_OF_SOURCE_ROWS: 0}

            join_keys = [index_col.name for e in feature_set.entities for index_col in e.index_columns]

            # deduplicate data
            df, has_dup = _deduplicate_dataframe(
                df=source_df, join_keys=join_keys, timestamp_column=feature_set.source.timestamp_column.name
            )
            number_of_materialized_rows = df.count() if has_dup else number_of_source_rows

            from pyspark.sql.functions import current_timestamp

            cur_time = current_timestamp()

            if feature_set.feature_transformation_code or CREATE_TIMESTAMP_COLUMN not in df.columns:
                df = df.withColumn(CREATE_TIMESTAMP_COLUMN, cur_time)

            df = df.withColumn(SYS_CREATE_TIMESTAMP_COLUMN, cur_time)
            df = df.withColumn(SYS_UPDATE_TIMESTAMP_COLUMN, cur_time)

            # materialize to online store
            number_of_online_materialized_rows = 0
            if feature_set.materialization_settings.online_enabled and feature_set.online_store:
                print(
                    "[Materialization Job] Materializing feature set: {}, version: {} into online store..".format(
                        feature_set.name, feature_set.version
                    )
                )
                number_of_online_materialized_rows = materialize_online(feature_set=feature_set, dataframe_to_store=df)

            # materialize to offline store
            number_of_offline_materialized_rows = 0
            if feature_set.materialization_settings.offline_enabled and feature_set.offline_store:
                print(
                    "[Materialization Job] Materializing feature set: {}, version: {} into offline store..".format(
                        feature_set.name, feature_set.version
                    )
                )
                feature_set.offline_store.write_data(feature_set=feature_set, df=df, upsert=upsert)
                number_of_offline_materialized_rows = number_of_materialized_rows

        return {
            NUMBER_OF_SOURCE_ROWS: number_of_source_rows,
            NUMBER_OF_OFFLINE_MATERIALIZED_ROWS: number_of_offline_materialized_rows,
            NUMBER_OF_ONLINE_MATERIALIZED_ROWS: number_of_online_materialized_rows,
        }
    except Exception as ex:
        if isinstance(ex, MlException):
            _get_logger().error(f"{PACKAGE_NAME}->Materialize, {type(ex).__name__}: {ex.no_personal_data_message}")
        else:
            _get_logger().error(f"{PACKAGE_NAME}->Materialize, {type(ex).__name__}: {ex}")

        log_and_raise_error(error=ex, debug=True)
