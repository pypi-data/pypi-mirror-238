# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from __future__ import annotations

import os
import logging
import re
import shutil
import uuid
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from azureml.dataprep.rslex import Copier
from azureml.featurestore._utils._constants import (
    AMLFEATURESTORE_EVENTLOG_ENABLED,
    AML_SDK_INSTRUMENTATION_KEY,
    AZURE_SERVICE,
    AZURE_SERVICE_VALUE,
    AZUREML_URI_PATTERNS,
    CLOUD_URI_PATTERNS,
    STORAGE_URI_PATTERNS,
)
from azureml.featurestore._utils.error_constants import (
    EMPTY_FEATURE_MESSAGE,
    FEATURE_NAME_COLLISION_MESSAGE,
    INVALID_FEATURE_URI_MESSAGE,
    SCHEMA_ERROR_MISSING_COLUMNS,
    UNSUPORTED_STORAGE_TYPE_MESSAGE,
)

from azure.ai.ml._artifacts._artifact_utilities import (
    download_artifact_from_aml_uri,
    download_artifact_from_storage_url,
)
from azure.ai.ml._telemetry.logging_handler import get_appinsights_log_handler, AzureMLSDKLogHandler
from azure.ai.ml._user_agent import USER_AGENT
from azure.ai.ml._utils._logger_utils import OpsLogger
from azure.ai.ml.entities._assets._artifacts.artifact import ArtifactStorageInfo
from azure.ai.ml.exceptions import ErrorCategory, ErrorTarget, ValidationErrorType, ValidationException
from azure.ai.ml.operations import DatastoreOperations

if TYPE_CHECKING:
    from azureml.featurestore._feature_set import FeatureSet
    from azureml.featurestore.contracts.feature import Feature


class PathType(Enum):
    azureml = 1
    cloud = 2
    local = 3
    storage = 4


def _process_path(path: str, datastore_operations: DatastoreOperations = None):
    path_type, base_path = _parse_path_format(path)
    if path_type == PathType.local:
        base_path = os.path.normpath(base_path)
        local_path = base_path
        if not os.path.isabs(base_path):
            local_path = os.path.join(os.getcwd(), base_path)
        if not os.path.exists(local_path):
            raise ValueError("File '%s' does not exist." % local_path)
    else:
        local_path = _download_file(path=path, path_type=path_type, datastore_operations=datastore_operations)

    return local_path


def _download_file(
    path: str,
    path_type: PathType,
    target_path: Optional[str] = None,
    datastore_operations: DatastoreOperations = None,
):
    from tempfile import mkdtemp

    # normalize path to yaml config path
    normalized_path = path.rstrip("/\\")
    local_path = mkdtemp() if not target_path else target_path

    if not datastore_operations:
        from azureml.dataprep.api._rslex_executor import ensure_rslex_environment
        from azureml.dataprep.rslex import PyIfDestinationExists, PyLocationInfo

        ensure_rslex_environment()

        if_destination_exists = PyIfDestinationExists.MERGE_WITH_OVERWRITE
        try:
            Copier.copy_uri(PyLocationInfo("Local", local_path, {}), normalized_path, if_destination_exists, "")
        except Exception as e:
            if "InvalidUriScheme" in e.args[0] or "DataAccessError(NotFound)" in e.args[0]:
                raise ValueError(f"{e.args[0]}, uri: {normalized_path}")
            elif "StreamError(NotFound)" in e.args[0]:
                raise ValueError(f"{e.args[0]}; Not able to find path: {normalized_path}")
            elif "PermissionDenied" in e.args[0]:
                raise PermissionError(f"{e.args[0]}; No permission to access path: {normalized_path}")
            else:
                raise SystemError(f"{e.args[0]}, uri: {normalized_path}")

        local_path = os.path.join(local_path, re.split(r"/|\\", normalized_path)[-1])
    else:
        if path_type == PathType.cloud:
            local_path = download_artifact_from_storage_url(
                blob_url=normalized_path,
                destination=local_path,
                datastore_operation=datastore_operations,
                datastore_name=None,
            )
        elif path_type == PathType.azureml:
            local_path = download_artifact_from_aml_uri(
                uri=normalized_path, destination=local_path, datastore_operation=datastore_operations
            )
        elif path_type == PathType.local:
            local_path = path
        else:
            raise Exception(
                f"Can't download from path: {normalized_path}, path type: {path_type.name} is not supported"
            )

    return local_path


def _ensure_azureml_full_path(path: str, subscription_id: str, resource_group: str, workspace_name: str):
    res = path
    if path.startswith("azureml://") and not path.startswith("azureml://subscriptions"):
        path = path.split("azureml://", 1)[1]
        res = f"azureml://subscriptions/{subscription_id}/resourcegroups/{resource_group}/workspaces/{workspace_name}/{path}"

    return res


def _parse_path_format(path: str):
    # TODO: include adl://|wasbs?://|abfss?:// when artifact download supports them
    regular_cloud_uri_patterns = re.compile(CLOUD_URI_PATTERNS, re.IGNORECASE)
    storage_uri_patterns = re.compile(STORAGE_URI_PATTERNS, re.IGNORECASE)
    azureml_uri_patterns = re.compile(AZUREML_URI_PATTERNS, re.IGNORECASE)

    if regular_cloud_uri_patterns.match(path):
        return PathType.cloud, path
    elif storage_uri_patterns.match(path):
        return PathType.storage, path
    elif azureml_uri_patterns.match(path):
        return PathType.azureml, path
    else:
        return PathType.local, path


def copy_rename_and_zip(path: str):
    from tempfile import gettempdir

    temp_name = uuid.uuid4().hex
    zip_path = os.path.join(gettempdir(), temp_name)
    dir_path = os.path.join(zip_path, temp_name)
    shutil.copytree(path, dir_path)
    return shutil.make_archive(zip_path, "zip", root_dir=zip_path)


def resolve_features(features: List[Feature]):
    from azureml.featurestore._feature_set import FeatureSet

    if not features:
        msg = EMPTY_FEATURE_MESSAGE
        raise ValidationException(
            message=msg,
            target=ErrorTarget.GENERAL,
            no_personal_data_message=msg,
            error_category=ErrorCategory.USER_ERROR,
            error_type=ValidationErrorType.MISSING_FIELD,
        )

    feature_references = []
    feature_sets = set()

    for f in features:
        feature_set = f.feature_set_reference
        if isinstance(feature_set, FeatureSet):
            feature_set.validate()
        feature_sets.add(feature_set)
        feature_references.append("{}:{}".format(feature_set.name, f.name))

    return feature_references, feature_sets


def validate_features(features: List[Feature]):
    feature_names = [f.name for f in features]
    collided_names = [f for f, occurrences in Counter(feature_names).items() if occurrences > 1]

    if len(collided_names) > 0:
        raise ValidationException(
            message=FEATURE_NAME_COLLISION_MESSAGE.format(collided_names),
            target=ErrorTarget.GENERAL,
            no_personal_data_message=FEATURE_NAME_COLLISION_MESSAGE,
            error_category=ErrorCategory.USER_ERROR,
        )


def feature_uri_parser_with_rename(uri):
    URI_REGEX_PATTERN = "^([^/]+):([^/]+):([^/]+)"

    match = re.match(URI_REGEX_PATTERN, uri)
    if match:
        return match.group(1), match.group(2), match.group(3)
    else:
        raise ValidationException(
            message=INVALID_FEATURE_URI_MESSAGE.format(uri),
            no_personal_data_message=INVALID_FEATURE_URI_MESSAGE.format("[uri]"),
            error_type=ValidationErrorType.INVALID_VALUE,
            error_category=ErrorCategory.USER_ERROR,
            target=ErrorTarget.ARM_RESOURCE,
        )


def _resolve_hdfs_path_from_storage_info(asset_artifact: ArtifactStorageInfo) -> str:
    DATALAKE_URL_GEN2_REGEX = r"([a-zA-Z0-9_\-]+).dfs.([a-zA-Z0-9.]+)"
    BLOB_URL_REGEX = r"([a-zA-Z0-9_\-]+).blob.([a-zA-Z0-9.]+)"
    DATALAKE_HDFS_FORMAT = "abfss://{}@{}.dfs.{}/{}"
    BLOB_HDFS_FORMAT = "wasbs://{}@{}.blob.{}/{}"

    adls_gen2_match = re.search(DATALAKE_URL_GEN2_REGEX, asset_artifact.storage_account_url)
    blob_match = re.search(BLOB_URL_REGEX, asset_artifact.storage_account_url)

    if adls_gen2_match:
        path = DATALAKE_HDFS_FORMAT.format(
            asset_artifact.container_name,
            adls_gen2_match.group(1),
            adls_gen2_match.group(2),
            asset_artifact.relative_path,
        )
        return path
    if blob_match:
        path = BLOB_HDFS_FORMAT.format(
            asset_artifact.container_name, blob_match.group(1), blob_match.group(2), asset_artifact.relative_path
        )
        return path

    raise ValidationException(
        message=UNSUPORTED_STORAGE_TYPE_MESSAGE.format(asset_artifact.storage_account_url),
        no_personal_data_message=UNSUPORTED_STORAGE_TYPE_MESSAGE,
        error_type=ValidationErrorType.INVALID_VALUE,
        error_category=ErrorCategory.USER_ERROR,
        target=ErrorTarget.ARM_RESOURCE,
    )


def get_temp_table_name(name) -> str:
    """Returns a random table name for temporary view"""
    return name + "_" + uuid.uuid4().hex


def build_offline_join_query(
    query_contexts, entity_table_name, entity_event_timestamp_col, entity_df_cols, query_template
):
    from jinja2 import BaseLoader, Environment

    template = Environment(loader=BaseLoader()).from_string(source=query_template)

    # Add additional fields to dict
    template_context = {
        "left_table_query_string": entity_table_name,
        "entity_df_event_timestamp_col": entity_event_timestamp_col,
        "unique_entity_keys": set([entity for c in query_contexts for entity in c.entities]),
        "featureviews": [asdict(context) for context in query_contexts],
    }

    query = template.render(template_context)
    return query


def validate_expected_columns_in_entity_df(entity_schema, timestamp_column, feature_sets: List[FeatureSet]):
    join_keys = set()
    for feature_set in feature_sets:
        for column in feature_set.get_index_columns():
            join_keys.add(column.name)

    entity_columns = set(entity_schema.keys())
    expected_columns = join_keys | {timestamp_column} if timestamp_column else join_keys
    missing_columns = expected_columns - entity_columns

    if len(missing_columns) > 0:
        raise ValidationException(
            message=SCHEMA_ERROR_MISSING_COLUMNS.format(expected_columns, missing_columns),
            no_personal_data_message=SCHEMA_ERROR_MISSING_COLUMNS,
            error_type=ValidationErrorType.INVALID_VALUE,
            error_category=ErrorCategory.USER_ERROR,
            target=ErrorTarget.ARM_RESOURCE,
        )


@dataclass(frozen=True)
class FeatureSetQueryContext:
    name: str
    temporal_lookback_seconds: int
    entities: List[str]
    features: List[str]
    event_timestamp_column: str
    created_timestamp_column: Optional[str]
    table_subquery: str
    entity_selections: List[str]
    min_event_timestamp: Optional[str]
    max_event_timestamp: str


def build_feature_set_query_context(feature_references, feature_sets, entity_df_timestamp_range):
    feature_set_to_features_map = get_feature_set_to_features_map(feature_sets, feature_references)
    query_context = []

    for feature_set, features in feature_set_to_features_map.items():
        join_keys = []
        entity_selections = []
        for index_column in feature_set.get_index_columns():
            join_key = index_column.name
            join_keys.append(join_key)
            entity_selections.append(f"{index_column.name} AS {join_key}")

        max_event_timestamp = entity_df_timestamp_range[1].isoformat()
        if feature_set.temporal_join_lookback:
            temporal_lookback = feature_set.temporal_join_lookback.to_timedelta()
            temporal_lookback_seconds = temporal_lookback.total_seconds()
            min_event_timestamp = (entity_df_timestamp_range[0] - temporal_lookback).isoformat()
        else:
            temporal_lookback_seconds = 0
            min_event_timestamp = None

        timestamp_column, _ = feature_set.get_timestamp_column()

        context = FeatureSetQueryContext(
            name=feature_set.name,
            temporal_lookback_seconds=temporal_lookback_seconds,
            entities=join_keys,
            features=features,
            event_timestamp_column=timestamp_column,
            created_timestamp_column=timestamp_column,
            table_subquery=f"{feature_set.name}_{feature_set.version}",
            entity_selections=entity_selections,
            min_event_timestamp=min_event_timestamp,
            max_event_timestamp=max_event_timestamp,
        )
        query_context.append(context)

    return query_context


def get_feature_set_to_features_map(feature_sets: List[FeatureSet], feature_references: List[str]):
    feature_set_to_features_map = defaultdict(list)

    for feature in feature_references:
        feature_set_name = feature.split(":")[0]
        feature_name = feature.split(":")[1]
        for feature_set in feature_sets:
            if feature_set.name == feature_set_name:
                feature_set_to_features_map[feature_set].append(feature_name)
                break

    return feature_set_to_features_map


def _build_logger(name: str):
    ops_logger = OpsLogger(name)
    app_insights_handler = get_appinsights_log_handler(user_agent=USER_AGENT)

    running_in_azure = os.getenv(AZURE_SERVICE, '').lower() == AZURE_SERVICE_VALUE
    default_enable_telemetry = 'true' if running_in_azure else 'false'
    enable_telemetry = os.getenv(AMLFEATURESTORE_EVENTLOG_ENABLED, default_enable_telemetry).lower() == 'true'

    if isinstance(app_insights_handler, logging.NullHandler) and enable_telemetry:
        app_insights_handler = _get_azuresdk_handler(name, enable_telemetry)

    app_insights_handler_kwargs = {"app_insights_handler": app_insights_handler}
    ops_logger.update_info(app_insights_handler_kwargs)
    return ops_logger.package_logger


def _get_azuresdk_handler(name, enable_telemetry=False):
    instrumentation_key = AML_SDK_INSTRUMENTATION_KEY
    custom_properties = {"name": name}
    custom_properties.update({"user_agent": USER_AGENT})
    return AzureMLSDKLogHandler(
        connection_string=f"InstrumentationKey={instrumentation_key}",
        custom_properties=custom_properties,
        enable_telemetry=enable_telemetry,)