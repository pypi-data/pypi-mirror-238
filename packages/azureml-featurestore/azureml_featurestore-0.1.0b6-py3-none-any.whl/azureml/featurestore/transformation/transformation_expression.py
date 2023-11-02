# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from abc import ABC, abstractmethod

from azureml.featurestore._utils._preview_method import _is_private_preview_enabled

from azure.ai.ml._utils._experimental import experimental

if _is_private_preview_enabled():

    @experimental
    class TransformationExpression(ABC):
        """Feature transformation expression representation"""

        @abstractmethod
        def _to_feathr_config(self):
            pass

        @abstractmethod
        def __repr__(self):
            pass

        @abstractmethod
        def __str__(self):
            pass
