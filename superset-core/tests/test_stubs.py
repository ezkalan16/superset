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

"""
Unit tests for the dependency-injected stubs.

These functions/classes intentionally raise ``NotImplementedError`` until the
host application replaces them during initialization. The tests pin that
contract so the placeholder never silently returns something usable.
"""

from __future__ import annotations

import pytest
from superset_core.mcp.decorators import prompt, tool
from superset_core.queries.query import get_sqlglot_dialect
from superset_core.rest_api.decorators import api
from superset_core.semantic_layers.decorators import semantic_layer
from superset_core.tasks.decorators import get_context, task, TaskWrapper


def test_api_decorator_is_uninitialized() -> None:
    with pytest.raises(NotImplementedError):
        api(id="main_api", name="Main API")


def test_semantic_layer_decorator_is_uninitialized() -> None:
    with pytest.raises(NotImplementedError):
        semantic_layer(id="dbt", name="dbt Semantic Layer")


def test_task_decorator_is_uninitialized() -> None:
    with pytest.raises(NotImplementedError):
        task(name="my_task")


def test_get_context_is_uninitialized() -> None:
    with pytest.raises(NotImplementedError):
        get_context()


def test_task_wrapper_methods_are_uninitialized() -> None:
    wrapper: TaskWrapper = TaskWrapper()

    with pytest.raises(NotImplementedError):
        wrapper()
    with pytest.raises(NotImplementedError):
        wrapper.schedule()


def test_mcp_tool_decorator_is_uninitialized() -> None:
    with pytest.raises(NotImplementedError):
        tool(name="my_tool")


def test_mcp_prompt_decorator_is_uninitialized() -> None:
    with pytest.raises(NotImplementedError):
        prompt(name="my_prompt")


def test_get_sqlglot_dialect_is_uninitialized() -> None:
    with pytest.raises(NotImplementedError):
        get_sqlglot_dialect(database=object())
