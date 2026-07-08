# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Unit tests for ``superset_core.semantic_layers.types``."""

from __future__ import annotations

import dataclasses

import isodate
import pyarrow as pa
import pytest
from superset_core.semantic_layers.types import (
    AggregationType,
    Dimension,
    Filter,
    Grain,
    Grains,
    Metric,
    Operator,
    OrderDirection,
    PredicateType,
    SemanticQuery,
)


def test_grain_validates_iso_duration() -> None:
    grain = Grain("Day", "P1D")

    assert grain.name == "Day"
    assert grain.representation == "P1D"


def test_grain_rejects_invalid_duration() -> None:
    with pytest.raises(isodate.ISO8601Error):
        Grain("Bad", "not-a-duration")


def test_grain_equality_and_hash_use_representation_only() -> None:
    # Names differ but representations match => equal and share a hash bucket.
    a = Grain("Day", "P1D")
    b = Grain("Daily", "P1D")
    c = Grain("Month", "P1M")

    assert a == b
    assert a != c
    assert hash(a) == hash(b)
    assert {a, b} == {a}


def test_grain_equality_with_other_type_is_not_implemented() -> None:
    assert (Grain("Day", "P1D").__eq__(object())) is NotImplemented


def test_grains_get_returns_registry_singleton() -> None:
    assert Grains.get("P1D") is Grains.DAY
    assert Grains.get("P1Y") is Grains.YEAR


def test_grains_get_builds_custom_grain_for_unknown_representation() -> None:
    custom = Grains.get("PT30S", name="HalfMinute")

    assert custom.name == "HalfMinute"
    assert custom.representation == "PT30S"
    # Not cached in the shared registry.
    assert Grains.get("PT30S") is not Grains.DAY


def test_grains_get_defaults_name_to_representation() -> None:
    custom = Grains.get("PT45S")

    assert custom.name == "PT45S"


def test_aggregation_and_operator_enum_values() -> None:
    assert AggregationType.SUM.value == "SUM"
    assert AggregationType("COUNT_DISTINCT") is AggregationType.COUNT_DISTINCT
    assert Operator.IN.value == "IN"
    assert Operator.IS_NULL.value == "IS NULL"


def test_dimension_and_metric_are_hashable_and_frozen() -> None:
    dimension = Dimension(id="d1", name="Country", type=pa.string())
    metric = Metric(
        id="m1",
        name="Total",
        type=pa.int64(),
        definition="SUM(sales)",
        aggregation=AggregationType.SUM,
    )

    # Frozen dataclasses are hashable and usable in sets.
    assert {dimension} == {dimension}
    assert metric.aggregation is AggregationType.SUM
    with pytest.raises(dataclasses.FrozenInstanceError):
        dimension.name = "Other"


def test_filter_is_ordered_and_hashable() -> None:
    dimension = Dimension(id="d1", name="Country", type=pa.string())
    flt = Filter(
        type=PredicateType.WHERE,
        column=dimension,
        operator=Operator.EQUALS,
        value="US",
    )

    assert flt in {flt}
    assert flt == Filter(
        type=PredicateType.WHERE,
        column=dimension,
        operator=Operator.EQUALS,
        value="US",
    )


def test_semantic_query_defaults() -> None:
    query = SemanticQuery(metrics=[], dimensions=[])

    assert query.filters is None
    assert query.order is None
    assert query.limit is None
    assert query.offset is None
    assert query.group_limit is None


def test_order_direction_values() -> None:
    assert OrderDirection.ASC.value == "ASC"
    assert OrderDirection.DESC.value == "DESC"
