# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import List

from azureml.featurestore._utils._preview_method import _is_private_preview_enabled
from jinja2 import Template

if _is_private_preview_enabled():

    def _to_feathr_join_config(
        timestamp_col_name: str,
        timestamp_col_format: str,
        feature_names: List[str],
        join_keys: List[str],
        start_time: str,
        end_time: str,
    ):
        feathr_join_tm = Template(
            # TODO: obsDataTimeSettings timeFormat should be configurable
            """
settings: {
observationDataTimeSettings: {
    absoluteTimeRange: {
        startTime: "{{start_time}}"
        endTime: "{{end_time}}"
        timeFormat: "yyyy-MM-dd HH:mm:ss"
    }
},
joinTimeSettings: {
    timestampColumn: {
        def: "{{timestamp_column}}"
        format: "{{timestamp_format}}"
    }
}
}
features: [
{
    key: [{{join_keys}}],
    featureList: [{{feature_names}}]
}
]
"""
        )
        feathr_join_string = feathr_join_tm.render(
            timestamp_column=timestamp_col_name,
            timestamp_format=timestamp_col_format,
            feature_names=", ".join(feature_names),
            join_keys=", ".join(join_keys),
            start_time=start_time,
            end_time=end_time,
        )

        return feathr_join_string

    def _to_feathr_fset_config(feature_sets: List):
        feathr_config_tm = Template(
            """
anchors: {
    {%- for feature_set in feature_sets %}
        {{feature_set._to_feathr_config("anchor")}}
    {%- endfor %}
}

sources: {
    {%- for feature_set in feature_sets %}
        {{feature_set._to_feathr_config("source")}}
    {%- endfor %}
}
"""
        )
        feathr_config_string = feathr_config_tm.render(feature_sets=feature_sets)

        return feathr_config_string

    def _to_feathr_anchor_config(feature_set_or_spec, join_keys: List[str]):
        anchor_tm = Template(
            """
"{{feature_set.name + "_" + feature_set.version + "_anchor"}}": {
    source: {{feature_set.name + "_" + feature_set.version + "_source"}}
    key: [{{join_keys}}]
    features: {
        {%- for feature in feature_set.feature_transformation.transformation_expressions %}
            {{feature._to_feathr_config()}}
        {%- endfor %}
    }
}
"""
        )
        anchor_string = anchor_tm.render(feature_set=feature_set_or_spec, join_keys=",".join(join_keys))
        return anchor_string

    def _to_feathr_source_config(feature_set_or_spec):
        source_name = feature_set_or_spec.name + "_" + feature_set_or_spec.version + "_source"
        source_string = feature_set_or_spec.source._to_feathr_config(source_name)
        return source_string
