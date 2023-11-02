# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import logging
import os
import time
from urllib.request import Request, urlopen

from azure.ai.ml.identity import CredentialUnavailableError
from azure.ai.ml.identity._internal import _scopes_to_resource
from azure.core.credentials import AccessToken, TokenCredential

_LOGGER = logging.getLogger(__name__)


class AzureMLHoboSparkOnBehalfOfCredential(TokenCredential):
    """Authenticates a user via the on-behalf-of flow on Hobo Spark compute.

    This credential can only be used on `Azure Machine Learning Hobo Spark Compute.`
    during job execution when user request to run job during its identity.
    """

    def __init__(self, **kwargs):
        provider_type = os.environ.get("AZUREML_DATAPREP_TOKEN_PROVIDER")
        if provider_type != "sparkobo":
            # OBO identity isn't available in this environment
            self._credential = None
        self._credential = _AzureMLHoboSparkOnBehalfOfCredential(**kwargs)

    def get_token(self, *scopes, **kwargs):
        """Request an access token for `scopes`.

        This method is called automatically by Azure SDK clients.

        :param str scopes: desired scope for the access token. This credential allows only one scope per request.
        :rtype: :class:`azure.core.credentials.AccessToken`
        :return: AzureML On behalf of credentials isn't available in the hosting environment
        :raises: ~azure.ai.ml.identity.CredentialUnavailableError
        """
        if not self._credential:
            raise CredentialUnavailableError(message=self.get_unavailable_message())

        return self._credential.get_token(*scopes, **kwargs)

    def get_unavailable_message(self):
        # type: () -> str
        return "AzureML On Behalf of credentials not available in this environment"


class _AzureMLHoboSparkOnBehalfOfCredential(object):
    def __init__(self, **kwargs):
        if len(kwargs) > 0:
            env_key_from_kwargs = [
                "AZUREML_SYNAPSE_CLUSTER_IDENTIFIER",
                "AZUREML_SYNAPSE_TOKEN_SERVICE_ENDPOINT",
                "AZUREML_RUN_ID",
                "AZUREML_RUN_TOKEN_EXPIRY",
            ]
            for env_key in env_key_from_kwargs:
                if env_key in kwargs.keys():
                    os.environ[env_key] = kwargs[env_key]
                else:
                    raise Exception("Unable to initialize AzureMLHoboSparkOBOCredential due to invalid arguments")
        else:
            from pyspark.sql import SparkSession

            try:
                spark = SparkSession.builder.getOrCreate()
            except Exception:
                raise Exception("Fail to get spark session, please check if spark environment is set up.")

            spark_conf = spark.sparkContext.getConf()
            spark_conf_vars = {
                "AZUREML_SYNAPSE_CLUSTER_IDENTIFIER": "spark.synapse.clusteridentifier",
                "AZUREML_SYNAPSE_TOKEN_SERVICE_ENDPOINT": "spark.tokenServiceEndpoint",
            }
            for env_key, conf_key in spark_conf_vars.items():
                value = spark_conf.get(conf_key)
                if value:
                    os.environ[env_key] = value

        self.obo_service_endpoint = os.environ.get("AZUREML_OBO_SERVICE_ENDPOINT")
        self.token_service_endpoint = os.environ.get("AZUREML_SYNAPSE_TOKEN_SERVICE_ENDPOINT")
        self.obo_access_token = os.environ.get("AZUREML_OBO_CANARY_TOKEN")
        self.cluster_identifier = os.environ.get("AZUREML_SYNAPSE_CLUSTER_IDENTIFIER")
        self.subscription_id = os.environ.get("AZUREML_ARM_SUBSCRIPTION")
        self.resource_group = os.environ.get("AZUREML_ARM_RESOURCEGROUP")
        self.workspace_name = os.environ.get("AZUREML_ARM_WORKSPACE_NAME")
        self.experiment_name = os.environ.get("AZUREML_ARM_PROJECT_NAME")
        self.run_id = os.environ.get("AZUREML_RUN_ID")
        self.oid = os.environ.get("OID")
        self.tid = os.environ.get("TID")

        if not self.obo_access_token:
            return None

    def get_token(self, *scopes, **kwargs):  # type: (*str, **Any) -> AccessToken
        resource = _scopes_to_resource(*scopes)
        request_url = "https://{}/api/v1/proxy/obotoken/v1.0/subscriptions/{}/resourceGroups/{}/providers/Microsoft.MachineLearningServices/workspaces/{}/getuseraccesstokenforspark".format(
            self.token_service_endpoint,
            self.subscription_id,
            self.resource_group,
            self.workspace_name,
        )

        request_body = {
            "oboToken": self.obo_access_token,
            "oid": self.oid,
            "tid": self.tid,
            "resource": resource,
            "experimentName": self.experiment_name,
            "runId": self.run_id,
        }

        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "x-ms-proxy-host": self.obo_service_endpoint,
            "obo-access-token": self.obo_access_token,
            "x-ms-cluster-identifier": self.cluster_identifier,
        }

        try:
            response = send_request(request_url, request_body, headers)
            if response:
                response_dict = json.loads(response.read().decode("utf-8"))
                access_token = AccessToken(response_dict["token"], int(time.time()) + 3600)
                return access_token

        except Exception as ex:
            _LOGGER.log(
                logging.WARNING,
                "%s.get_token failed: %s",
                self.__class__.__name__,
                ex,
                exc_info=_LOGGER.isEnabledFor(logging.DEBUG),
            )
            raise


def send_request(url, data=None, headers=None, method=None):
    args = {"url": url}
    if data:
        data = json.dumps(data)
        args["data"] = data.encode("utf8")
    if headers:
        args["headers"] = headers
    if method:
        # the default is GET if data is None, POST otherwise
        args["method"] = method

    return urlopen(Request(**args), timeout=5)
