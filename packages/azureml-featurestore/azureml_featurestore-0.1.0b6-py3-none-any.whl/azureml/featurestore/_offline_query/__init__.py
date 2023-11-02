# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

from .._utils._preview_method import _is_private_preview_enabled
from .offline_retrieval_job import OfflineRetrievalJob
from .point_at_time import PointAtTimeRetrievalJob

__all__ = [
    "OfflineRetrievalJob",
    "PointAtTimeRetrievalJob",
]

if _is_private_preview_enabled():
    from .dsl_feathr_retrieval_job import DslFeathrRetrievalJob

    __all__.append("DslFeathrRetrievalJob")
