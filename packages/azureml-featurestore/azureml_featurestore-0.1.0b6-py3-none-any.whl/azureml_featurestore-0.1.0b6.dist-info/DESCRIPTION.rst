# Azure Machine Learning Feature Store Python SDK

The `azureml-featurestore` package is the core SDK interface for Azure ML Feature Store. This SDK works along the 
`azure-ai-ml` SDK to provide the managed feature store experience.

## Main features in the `azureml-featurestore` package
- Develop feature set specification in Spark with the ability for feature transformation.
- List and get feature sets defined in Azure  ML Feature Store.
- Generate and resolve feature retrieval specification.
- Run offline feature retrieval with point-in-time join.

## Getting started

You can install the package via ` pip install azureml-featurestore `

To learn more about Azure ML managed feature store visit https://aka.ms/featurestore-get-started


# Change Log
## 0.1.0b6 (2023.11.1)

- Various bug fixes

## 0.1.0b5 (2023.10.4)

- Various bug fixes

## 0.1.0b4 (2023.08.28)

**New Features:**

- [Public preview] Added custom feature source. Custom feature source supports customized source process code script with a user defined dictionary as input.
- [Public preview] Added csv feature source, deltatable feature source, mltable feature source, parquet feature source as new feature source experience. Previous feature source usage compatibility will be deprecated in 6 months.

- Bug fixes

**Breaking changes:**
- Moved `init_online_lookup`, `shutdown_online_lookup` and `get_online_features` out of FeatureStoreClient, and into the module as standalone functions.
- `get_online_features` contract changed from accepting (for the `observation_data` argument) and returning `pandas.DataFrame` to accepting (as the `observation_data` argument) and returning `pyarrow.Table`.

**Other changes:**
- Moved online feature store support into public preview.

## 0.1.0b3 (2023.07.10)

- Various bug fixes

## 0.1.0b2 (2023.06.13)

**New Features:**

- [Private preview] Added online store support. Online store supports materialization and online feature values retrieval from Redis cache for batch scoring.

- Various bug fixes

## 0.1.0b1 (2023.05.15)

**New Features:**

Initial release.
