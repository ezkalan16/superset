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

"""Unit tests for ``superset_core.tasks.types``."""

from __future__ import annotations

import dataclasses

import pytest
from superset_core.tasks.types import (
    TaskOptions,
    TaskProperties,
    TaskScope,
    TaskStatus,
)


def test_task_status_values() -> None:
    assert TaskStatus.PENDING.value == "pending"
    assert TaskStatus("aborted") is TaskStatus.ABORTED
    assert {s.value for s in TaskStatus} == {
        "pending",
        "in_progress",
        "success",
        "failure",
        "aborting",
        "aborted",
        "timed_out",
    }


def test_task_scope_values() -> None:
    assert TaskScope.PRIVATE.value == "private"
    assert TaskScope.SHARED.value == "shared"
    assert TaskScope.SYSTEM.value == "system"


def test_task_status_is_string_enum() -> None:
    # ``str`` mixin means the member compares equal to its string value.
    assert TaskStatus.SUCCESS == "success"


def test_task_options_defaults() -> None:
    options = TaskOptions()

    assert options.task_key is None
    assert options.task_name is None
    assert options.timeout is None


def test_task_options_is_dataclass() -> None:
    assert dataclasses.is_dataclass(TaskOptions)


def test_task_options_is_frozen() -> None:
    options = TaskOptions(task_key="k", task_name="n", timeout=60)

    with pytest.raises(dataclasses.FrozenInstanceError):
        options.timeout = 120


def test_task_options_equality() -> None:
    assert TaskOptions(task_key="k") == TaskOptions(task_key="k")
    assert TaskOptions(task_key="k") != TaskOptions(task_key="other")


def test_task_properties_is_sparse_typed_dict() -> None:
    # ``total=False`` means partial dicts are valid instances at runtime.
    props: TaskProperties = {"is_abortable": True, "progress_percent": 0.5}

    assert props.get("is_abortable") is True
    assert props.get("timeout") is None
