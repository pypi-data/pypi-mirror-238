# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import unittest

import pytest
from azureml.featurestore.contracts import DateTimeOffset
from azureml.featurestore.transformation.aggregation_function import AggregationFunction
from azureml.featurestore.transformation.window_aggregation import WindowAggregation


@pytest.mark.unittest
class TransformationTest(unittest.TestCase):
    def test_window_aggregation(self):
        rwa = WindowAggregation(
            feature_name="3d_sum_of_column1",
            source_column="column1",
            aggregation=AggregationFunction.SUM,
            window=DateTimeOffset(3, 0, 0),
        )

        assert rwa
        feathr_str = """
3d_sum_of_column1: {
    def: column1
    aggregation: SUM
    window: 3d
}"""
        self.assertEquals(feathr_str, rwa._to_feathr_config())

    def test_window_aggregation_with_string_aggregation(self):
        rwa = WindowAggregation(
            feature_name="3d_sum_of_column1",
            source_column="column1",
            aggregation="sum",
            window=DateTimeOffset(3, 0, 0),
        )

        assert rwa
        feathr_str = """
3d_sum_of_column1: {
    def: column1
    aggregation: SUM
    window: 3d
}"""
        print(rwa._to_feathr_config())
        self.assertEquals(feathr_str, rwa._to_feathr_config())

    def test_window_aggregation_with_invalid_aggregation(self):
        with self.assertRaises(ValueError):
            WindowAggregation(
                feature_name="3d_sum_of_column1",
                source_column="column1",
                aggregation="SUMM",
                window=DateTimeOffset(3, 0, 0),
            )
