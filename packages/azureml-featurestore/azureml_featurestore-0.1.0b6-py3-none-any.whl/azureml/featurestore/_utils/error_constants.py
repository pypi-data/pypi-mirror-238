# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# schema errors
SCHEMA_ERROR_NO_TIMESTAMP_COLUMN = "Schema check errors, timestamp column: {} is not in output dataframe"
SCHEMA_ERROR_NO_INDEX_COLUMN = "Schema check errors, no index column: {} in output dataframe"
SCHEMA_ERROR_WRONG_DATA_TYPE = "Schema check errors, column: {} has data type: {}, expected: {}"
SCHEMA_ERROR_MISSING_COLUMNS = "Expected entity and timestamp columns not found. Expected: {}. Missing: {}"
REFER_FEATURE_SET_SPEC_SCHEMA = "Please refer to the source section in https://learn.microsoft.com/en-us/azure/machine-learning/reference-yaml-featureset-spec?view=azureml-api-2"

# resolve feature errors
EMPTY_FEATURE_MESSAGE = "Feature list must be non-empty."
FEATURE_NAME_COLLISION_MESSAGE = "There are feature name collisions. Duplicate features: {}"
INVALID_FEATURE_URI_MESSAGE = (
    'Invalid feature reference {}. Feature reference must be in the form "<feature_set>:<version>:<feature_name>"'
)

# storage errors
UNSUPORTED_STORAGE_TYPE_MESSAGE = "Unsupported Storage account type. Storage url: {}"

# feature set spec errors
MISSING_FEATURE_SOURCE = "Feature source is required for a feature set, please provide a feature source"
MISSING_INDEX_COLUMN = "Index columns is required for a feature set, please provide non empty index columns"
MISSING_TIMESTAMP_COLUMN = "Expected timestamp columns not found in feature set {}."
FEATURE_NAME_NOT_STRING = "Name must be the string name of a feature in this feature set spec. Found: {}"
FEATURE_NAME_NOT_FOUND = "Feature '{}' not found in this feature set spec."

# feature set errors
FEATURE_NAME_NOT_STRING_FEATURE_SET = "Name must be the string name of a feature in this feature set. Found: {}"
FEATURE_NAME_NOT_FOUND_FEATURE_SET = "Feature '{}' not found in this feature set."
FEATURE_SET_NOT_REGISTERED = "Feature Set object must be registered as asset to do this operation."

OFFLINE_MATERIALIZATION_DISABLED = "Feature set {}, version {}, offline materialization has been disabled" 
ONLINE_MATERIALIZATION_DISABLED = "Feature set {}, version {}, online materialization has been disabled" 

# feature source
SOURCE_TYPE_NOT_SUPPORTED = (
    "Invalid schema for feature source. Feature source type: {} is not supported." + REFER_FEATURE_SET_SPEC_SCHEMA
)
SIMPLE_SOURCE_VALIDATION = (
    "Invalid schema for feature source. Only path should be provided when source type is {}."
    + REFER_FEATURE_SET_SPEC_SCHEMA
)
CUSTOM_SOURCE_VALIDATION = (
    "Invalid schema for feature source. Only kwargs and source_process_code should be provided when source type is custom."
    + REFER_FEATURE_SET_SPEC_SCHEMA
)

# feature store client errors
NOT_A_FEATURE_STORE = "{} is not a Feature Store workspace."
FEATURE_WRONG_TYPE = "Features must be of type 'Feature'. Did you run `resolve_feature_uri()`?"
FEATURE_STORE_CLIENT_INCORRECT_SETUP = (
    "FeatureStoreClient was not configured with subscription, resource group and workspace information"
)
UNSUPPORTED_QUERY_MODE = "Query mode {} is not supported."

# i/o errors
DESTINATION_NOT_LOCAL_PATH = "Destination {} must be local path"
DESTINATION_NOT_EXIST = "Destination {} must be an existing folder path"
FILE_ALREADY_EXIST = "File {} already exists"
PATH_NOT_EXISTING_FOLDER = "Path {} must be an existing folder path"

# connection name validation errors
OFFLINE_CONNECTION_NAME_MISTMACH = "Offline store has been updated, please re-enable offline materialization" 
ONLINE_CONNECTION_NAME_MISMATCH = "Online store has been updated, please re-enable online materialization"