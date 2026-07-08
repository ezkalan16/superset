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

"""Unit tests for ``superset_core.queries.types``."""

from __future__ import annotations

import pytest
from superset_core.queries.types import (
    AsyncQueryHandle,
    CacheOptions,
    QueryOptions,
    QueryResult,
    QueryStatus,
    StatementResult,
)


def test_query_status_values() -> None:
    assert QueryStatus.SUCCESS.value == "success"
    assert QueryStatus("failed") is QueryStatus.FAILED
    assert {s.value for s in QueryStatus} == {
        "pending",
        "running",
        "success",
        "failed",
        "timed_out",
        "stopped",
    }


def test_cache_options_defaults() -> None:
    options = CacheOptions()

    assert options.timeout is None
    assert options.force_refresh is False


def test_query_options_defaults() -> None:
    options = QueryOptions()

    assert options.catalog is None
    assert options.schema is None
    assert options.limit is None
    assert options.timeout_seconds is None
    assert options.template_params is None
    assert options.cache is None
    assert options.dry_run is False


def test_query_options_accepts_values() -> None:
    options = QueryOptions(
        catalog="cat",
        schema="public",
        limit=100,
        template_params={"table": "events"},
        cache=CacheOptions(timeout=60, force_refresh=True),
        dry_run=True,
    )

    assert options.schema == "public"
    assert options.limit == 100
    assert options.template_params == {"table": "events"}
    assert options.cache.force_refresh is True
    assert options.dry_run is True


def test_statement_result_defaults() -> None:
    result = StatementResult(original_sql="SELECT 1", executed_sql="SELECT 1")

    assert result.data is None
    assert result.row_count == 0
    assert result.execution_time_ms is None


def test_query_result_defaults() -> None:
    result = QueryResult(status=QueryStatus.SUCCESS)

    assert result.statements == []
    assert result.query_id is None
    assert result.total_execution_time_ms is None
    assert result.is_cached is False
    assert result.error_message is None


def test_query_result_statements_are_independent() -> None:
    # ``statements`` uses a default_factory, so instances must not share a list.
    first = QueryResult(status=QueryStatus.SUCCESS)
    second = QueryResult(status=QueryStatus.SUCCESS)
    first.statements.append(
        StatementResult(original_sql="SELECT 1", executed_sql="SELECT 1")
    )

    assert second.statements == []


def test_async_query_handle_defaults_and_stub_methods() -> None:
    handle = AsyncQueryHandle(query_id=1)

    assert handle.status is QueryStatus.PENDING
    assert handle.started_at is None
    for method in (handle.get_status, handle.get_result, handle.cancel):
        with pytest.raises(NotImplementedError):
            method()
