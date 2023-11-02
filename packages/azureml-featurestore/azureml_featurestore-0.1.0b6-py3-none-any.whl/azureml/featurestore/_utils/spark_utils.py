# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from datetime import datetime
from typing import List, Tuple

from azureml.featurestore._utils._constants import (
    CREATE_TIMESTAMP_COLUMN,
    PARTITION_COLUMN,
    SYS_CREATE_TIMESTAMP_COLUMN,
    SYS_UPDATE_TIMESTAMP_COLUMN,
)
from azureml.featurestore._utils.error_constants import (
    SCHEMA_ERROR_NO_INDEX_COLUMN,
    SCHEMA_ERROR_NO_TIMESTAMP_COLUMN,
    SCHEMA_ERROR_WRONG_DATA_TYPE,
)
from azureml.featurestore._utils.type_map import TypeMap
from azureml.featurestore.contracts.feature import Feature
from azureml.featurestore.contracts.partition import Partition
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, lit, rand, row_number, to_timestamp
from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window

from azure.ai.ml.entities import DataColumn
from azure.ai.ml.exceptions import ErrorCategory, ErrorTarget, ValidationErrorType, ValidationException


def _filter_dataframe(
    spark: SparkSession,
    df: DataFrame,
    feature_window_start_date_time: datetime,
    feature_window_end_date_time: datetime,
    index_columns: List[str],
    timestamp_column: str,
    features: List[str],
) -> DataFrame:
    # filter the dataframe to the given feature window and remove intermediate rows from source lookback (if any)
    if feature_window_start_date_time:
        df = df.filter(col(timestamp_column) >= to_timestamp(lit(feature_window_start_date_time)))

    if feature_window_end_date_time:
        df = df.filter(col(timestamp_column) < to_timestamp(lit(feature_window_end_date_time)))

    columns = index_columns
    if CREATE_TIMESTAMP_COLUMN in df.columns:
        columns.append(CREATE_TIMESTAMP_COLUMN)
    if timestamp_column:
        columns.append(timestamp_column)
    columns += features

    df = df.select(*columns)

    return df


def _source_schema_check(df: DataFrame, features: List[Feature], index_columns: List[DataColumn]):
    for feature in features:
        if feature.name not in df.columns:
            raise Exception("Schema check errors, no feature column: {} in output dataframe".format(feature.name))
        data_type = TypeMap.spark_to_column_type(df.schema[feature.name].dataType.typeName())
        expected_data_type = feature.type
        if data_type != expected_data_type:
            raise ValidationException(
                message=SCHEMA_ERROR_WRONG_DATA_TYPE.format(feature.name, data_type, expected_data_type),
                no_personal_data_message=SCHEMA_ERROR_WRONG_DATA_TYPE,
                error_type=ValidationErrorType.MISSING_FIELD,
                error_category=ErrorCategory.USER_ERROR,
                target=ErrorTarget.GENERAL,
            )

    for index_column in index_columns:
        if index_column.name not in df.columns:
            raise Exception(SCHEMA_ERROR_NO_INDEX_COLUMN.format(index_column.name))
        data_type = TypeMap.spark_to_column_type(df.schema[index_column.name].dataType.typeName())
        expected_data_type = index_column.type
        if data_type != expected_data_type:
            raise ValidationException(
                message=SCHEMA_ERROR_WRONG_DATA_TYPE.format(index_column.name, data_type, expected_data_type),
                no_personal_data_message=SCHEMA_ERROR_WRONG_DATA_TYPE,
                error_type=ValidationErrorType.MISSING_FIELD,
                error_category=ErrorCategory.USER_ERROR,
                target=ErrorTarget.GENERAL,
            )

    return df, list(map(lambda i: i.name, index_columns))


def _source_timestamp_check(
    df: DataFrame,
    timestamp_column: str,
    timestamp_column_format: str,
):
    if not timestamp_column:
        return df, timestamp_column

    if timestamp_column in df.columns:
        if df.schema[timestamp_column].dataType != TimestampType():
            if timestamp_column_format:
                df = df.withColumn(timestamp_column, to_timestamp(timestamp_column, timestamp_column_format))
            else:
                df = df.withColumn(timestamp_column, to_timestamp(timestamp_column))
    else:
        raise ValidationException(
            message=SCHEMA_ERROR_NO_TIMESTAMP_COLUMN.format(timestamp_column),
            no_personal_data_message=SCHEMA_ERROR_NO_TIMESTAMP_COLUMN,
            error_type=ValidationErrorType.MISSING_FIELD,
            error_category=ErrorCategory.USER_ERROR,
            target=ErrorTarget.GENERAL,
        )

    return df, timestamp_column


def infer_event_timestamp_range(observation_data: DataFrame, timestamp_column: str):
    min_time = observation_data.agg({timestamp_column: "min"}).collect()[0][0]
    max_time = observation_data.agg({timestamp_column: "max"}).collect()[0][0]
    if isinstance(min_time, str):
        import pandas as pd

        min_time = pd.to_datetime(min_time, utc=True).to_pydatetime()
        max_time = pd.to_datetime(max_time, utc=True).to_pydatetime()
    event_timestamp_range = (min_time, max_time)

    return event_timestamp_range


def _deduplicate_dataframe(df: DataFrame, join_keys: List[str], timestamp_column: str) -> Tuple[DataFrame, bool]:
    # check duplicated rows in input data, and help deduplicate
    if len(df.groupBy(join_keys + [timestamp_column]).count().filter(col("count") > 1).take(1)) > 0:
        if CREATE_TIMESTAMP_COLUMN in df.columns:
            w2 = Window.partitionBy(join_keys + [timestamp_column]).orderBy(col(CREATE_TIMESTAMP_COLUMN).desc())
        else:
            w2 = Window.partitionBy(join_keys + [timestamp_column]).orderBy(rand())
        distinct_df = df.withColumn("row", row_number().over(w2)).filter(col("row") == 1).drop("row")

        return distinct_df, True
    else:
        return df, False


def build_update_feature_mapping(source_prefix, feature_names):
    mapping = {
        CREATE_TIMESTAMP_COLUMN: f"{source_prefix}.{CREATE_TIMESTAMP_COLUMN}",
        SYS_UPDATE_TIMESTAMP_COLUMN: f"{source_prefix}.{SYS_UPDATE_TIMESTAMP_COLUMN}",
    }
    for feature_name in feature_names:
        mapping[feature_name] = f"{source_prefix}.{feature_name}"

    return mapping


def build_insert_feature_mapping(source_prefix, join_keys, feature_names, timestamp_column):
    mapping = build_update_feature_mapping(source_prefix, feature_names)
    mapping[SYS_CREATE_TIMESTAMP_COLUMN] = f"{source_prefix}.{SYS_CREATE_TIMESTAMP_COLUMN}"
    mapping[timestamp_column] = f"{source_prefix}.{timestamp_column}"
    mapping[PARTITION_COLUMN] = f"{source_prefix}.{PARTITION_COLUMN}"

    for join_key in join_keys:
        mapping[join_key] = f"{source_prefix}.{join_key}"

    return mapping


def build_merge_condition(join_keys, source_prefix, target_prefix, timestamp_column, partition_list):
    partition_str = ",".join(f"'{partition}'" for partition in partition_list)
    arr = [
        f"{target_prefix}.{PARTITION_COLUMN} IN ({partition_str})",
        f"{source_prefix}.{timestamp_column} = {target_prefix}.{timestamp_column}",
    ]
    for join_key in join_keys:
        arr.append(f"{source_prefix}.{join_key} = {target_prefix}.{join_key}")
    return " AND ".join(arr)


def build_updated_timestamp_merge_condition(source_prefix, target_prefix):
    return f"{source_prefix}.{CREATE_TIMESTAMP_COLUMN} > {target_prefix}.{CREATE_TIMESTAMP_COLUMN}"


def build_partition_list(partition: Partition):
    # place holder for changing partition strategy
    return partition.partition_column
