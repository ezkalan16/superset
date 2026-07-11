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

"""Unit tests for the abstract semantic-layer/task base classes."""

from __future__ import annotations

import pytest
from superset_core.semantic_layers.layer import SemanticLayer
from superset_core.semantic_layers.view import SemanticView, SemanticViewFeature
from superset_core.tasks.types import TaskContext


def test_semantic_view_feature_values() -> None:
    assert SemanticViewFeature.GROUP_LIMIT.value == "GROUP_LIMIT"
    assert {f.value for f in SemanticViewFeature} == {
        "ADHOC_EXPRESSIONS_IN_ORDERBY",
        "GROUP_LIMIT",
        "GROUP_OTHERS",
    }


def test_semantic_view_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        SemanticView()


def test_semantic_layer_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        SemanticLayer()


def test_task_context_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        TaskContext()


def test_concrete_semantic_view_must_implement_all_abstract_methods() -> None:
    class PartialView(SemanticView):
        def uid(self) -> str:
            return "partial"

    # Missing the remaining abstract methods => still not instantiable.
    with pytest.raises(TypeError):
        PartialView()
