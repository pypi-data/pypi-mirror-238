# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import datetime
from typing import TYPE_CHECKING

from azureml.featurestore._feature_set import FeatureSet
from azureml.featurestore._utils._constants import MAXIMUM_MATERIALIZATION_RETRY_TIMES, PACKAGE_NAME
from azureml.featurestore._utils.arm_id_utils import OfflineStoreTargetArmId
from azureml.featurestore._utils.error_constants import (
    OFFLINE_CONNECTION_NAME_MISTMACH,
    OFFLINE_MATERIALIZATION_DISABLED,
)
from azureml.featurestore._utils.utils import _build_logger
from azureml.featurestore.contracts.offline_store import OfflineStore

from azure.ai.ml._exception_helper import log_and_raise_error
from azure.ai.ml._telemetry.activity import ActivityType, monitor_with_activity
from azure.ai.ml._utils._arm_id_utils import AMLVersionedArmId
from azure.ai.ml.exceptions import ErrorCategory, ErrorTarget, MlException, ValidationErrorType, ValidationException

if TYPE_CHECKING:
    from pyspark.sql import DataFrame

package_logger = None


def _get_logger():
    global package_logger
    if package_logger is None:
        package_logger = _build_logger(__name__)
    return package_logger


class AzureDataLakeOfflineStore(OfflineStore):
    def __init__(self, target: str, connection_name: str, location: str):
        self.__location = location
        super().__init__(target=target, connection_name=connection_name)

    def read_data(
        self,
        feature_set: FeatureSet,
        feature_window_start_time: datetime = None,
        feature_window_end_time: datetime = None,
        **kwargs,
    ) -> "DataFrame":
        if not feature_set.materialization_settings.offline_enabled:
            raise Exception(OFFLINE_MATERIALIZATION_DISABLED.format(feature_set.name, feature_set.version))

        if self.connection_name != feature_set.offline_store_connection_name:
            raise ValidationException(
                message=OFFLINE_CONNECTION_NAME_MISTMACH,
                no_personal_data_message=OFFLINE_CONNECTION_NAME_MISTMACH,
                error_type=ValidationErrorType.INVALID_VALUE,
                error_category=ErrorCategory.USER_ERROR,
                target=ErrorTarget.GENERAL,
            )

        materialization_version = kwargs.get("materialization_version", None)

        df = self.validate_data(
            feature_set=feature_set,
            feature_window_start_time=feature_window_start_time,
            feature_window_end_time=feature_window_end_time,
            materialization_version=materialization_version,
        )
        if not df:
            return None

        from pyspark.sql.functions import col, lit, to_timestamp

        partition_column = feature_set.partition.partition_column

        if feature_window_start_time:
            feature_window_start_partition = feature_set.partition.get_partition(feature_window_start_time)
            df = df.filter(col(partition_column) >= lit(feature_window_start_partition))
            df = df.filter(
                col(feature_set.source.timestamp_column.name) >= to_timestamp(lit(feature_window_start_time))
            )

        if feature_window_end_time:
            feature_window_end_partition = feature_set.partition.get_partition(feature_window_end_time)
            df = df.filter(col(partition_column) <= lit(feature_window_end_partition))
            df = df.filter(col(feature_set.source.timestamp_column.name) < to_timestamp(lit(feature_window_end_time)))

        return df

    @monitor_with_activity(_get_logger(), f"{PACKAGE_NAME}->OfflineStore.WriteData", ActivityType.PUBLICAPI)
    def write_data(
        self,
        feature_set: FeatureSet,
        df: "DataFrame" = None,
        feature_window_start_time: datetime = None,
        feature_window_end_time: datetime = None,
        **kwargs,
    ) -> int:
        upsert = kwargs.get("upsert", False)
        replace = kwargs.get("replace", False)
        materialization_version = kwargs.get("materialization_version", None)

        try:
            if not feature_set.materialization_settings.offline_enabled:
                raise Exception(OFFLINE_MATERIALIZATION_DISABLED.format(feature_set.name, feature_set.version))

            if self.connection_name != feature_set.offline_store_connection_name:
                raise ValidationException(
                    message=OFFLINE_CONNECTION_NAME_MISTMACH,
                    no_personal_data_message=OFFLINE_CONNECTION_NAME_MISTMACH,
                    error_type=ValidationErrorType.INVALID_VALUE,
                    error_category=ErrorCategory.USER_ERROR,
                    target=ErrorTarget.GENERAL,
                )

            from azureml.featurestore._utils.spark_utils import (
                build_insert_feature_mapping,
                build_merge_condition,
                build_update_feature_mapping,
                build_updated_timestamp_merge_condition,
            )
            from delta.exceptions import ConcurrentAppendException
            from delta.tables import DeltaTable
            from pyspark.sql import SparkSession

            if not df:
                return 0

            spark = SparkSession.builder.getOrCreate()

            timestamp_column, _ = feature_set.get_timestamp_column()
            partition_column = feature_set.partition.partition_column

            partitions = [partition_column]

            table_path = self.__get_offline_store_table_path(
                OfflineStoreTargetArmId(self.target),
                feature_set.arm_id,
                materialization_version=materialization_version,
            )

            df = feature_set.partition.apply_partition(df=df)
            partition_list = df.select(partition_column).distinct().rdd.flatMap(lambda x: x).collect()

            join_keys = [index_col.name for e in feature_set.entities for index_col in e.index_columns]
            feature_names = [feature.name for feature in feature_set.features]

            number_of_materialized_rows = df.count()
            print(
                f"[Materialization Job] Ingest feature set: {feature_set.name}, version: {feature_set.version} data into offline store: {self.target}"
            )
            table_exist = (
                True
                if self.validate_data(feature_set=feature_set, materialization_version=materialization_version)
                else False
            )
            for i in range(0, MAXIMUM_MATERIALIZATION_RETRY_TIMES):
                try:
                    if not table_exist:
                        print(
                            f"[Materialization Job] Creating new table: {feature_set.name}, version: {feature_set.version}"
                        )
                        df.write.partitionBy(partitions).format("delta").mode("overwrite").save(table_path)
                    else:
                        if not upsert:
                            print(
                                f"[Materialization Job] Appending data to existing table: {feature_set.name}, version: {feature_set.version}"
                            )
                            df.write.partitionBy(partitions).format("delta").mode("append").save(table_path)
                        elif replace:
                            print(
                                f"[Materialization Job] Overwrite data in existing table: {feature_set.name}, version: {feature_set.version}"
                            )
                            condition = f"{timestamp_column} >= '{feature_window_start_time}' AND {timestamp_column} < '{feature_window_end_time}'"
                            df.write.mode("overwrite").format("delta").option("replaceWhere", condition).save(
                                table_path
                            )
                        else:
                            print(
                                f"[Materialization Job] Merging data into existing table: {feature_set.name}, version: {feature_set.version}"
                            )
                            target_table_alias = "{}_{}".format(feature_set.name, feature_set.version)
                            updates_alias = "{}_updates".format(target_table_alias)

                            merge_conditions = build_merge_condition(
                                join_keys, updates_alias, target_table_alias, timestamp_column, partition_list
                            )

                            updated_timestamp_merge_conditions = build_updated_timestamp_merge_condition(
                                updates_alias, target_table_alias
                            )
                            materialized_table = DeltaTable.forPath(spark, table_path)

                            update_mapping = build_update_feature_mapping(updates_alias, feature_names)
                            insert_mapping = build_insert_feature_mapping(
                                updates_alias, join_keys, feature_names, timestamp_column
                            )

                            materialized_table.alias(target_table_alias).merge(
                                source=df.alias(updates_alias), condition=merge_conditions
                            ).whenMatchedUpdate(
                                condition=updated_timestamp_merge_conditions, set=update_mapping
                            ).whenNotMatchedInsert(
                                values=insert_mapping
                            ).execute()
                except ConcurrentAppendException:
                    print(
                        f"[Materialization Job] Warning: hit concurrent operation exception when ingesting data, retry: {i + 1}"
                    )
                    continue
                break

            return number_of_materialized_rows
        except Exception as ex:
            if isinstance(ex, MlException):
                _get_logger().error(
                    f"{PACKAGE_NAME}->OfflineStore.WriteData, {type(ex).__name__}: {ex.no_personal_data_message}"
                )
            else:
                _get_logger().error(f"{PACKAGE_NAME}->OfflineStore.WriteData, {type(ex).__name__}: {ex}")

            log_and_raise_error(error=ex, debug=True)

    def validate_data(
        self,
        feature_set: FeatureSet,
        feature_window_start_time: datetime = None,
        feature_window_end_time: datetime = None,
        materialization_version: str = None,
    ) -> "DataFrame":
        from pyspark.sql import SparkSession
        from pyspark.sql.utils import AnalysisException

        spark = SparkSession.builder.getOrCreate()

        materialized_path = self.__get_offline_store_table_path(
            OfflineStoreTargetArmId(self.target), feature_set.arm_id, materialization_version=materialization_version
        )
        try:
            df = spark.read.format("delta").load(materialized_path)
            return df
        except AnalysisException as ae:
            if "not exist" in str(ae) or "not a Delta table" in str(ae):
                return None
            else:
                raise

    def __get_offline_store_table_path(
        self,
        offline_store_arm_id: OfflineStoreTargetArmId,
        feature_set_version_arm_id: AMLVersionedArmId,
        materialization_version: str = None,
    ):
        feature_store_id = "{}_{}_{}".format(
            feature_set_version_arm_id.workspace_name,
            feature_set_version_arm_id.subscription_id,
            feature_set_version_arm_id.resource_group_name,
        )

        path = "{}/{}/{}/{}".format(
            offline_store_arm_id.to_abfs_path(self.__location),
            feature_store_id,
            feature_set_version_arm_id.asset_name,
            feature_set_version_arm_id.asset_version,
        )

        if materialization_version:
            path = "{}/{}/{}/{}/{}".format(
                offline_store_arm_id.to_abfs_path(self.__location),
                feature_store_id,
                "materialize_store",
                feature_set_version_arm_id.asset_name,
                feature_set_version_arm_id.asset_version,
            )
            path = "{}/{}".format(path, materialization_version)

        return path.lower()
