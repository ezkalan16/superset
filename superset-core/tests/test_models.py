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

"""Unit tests for the abstract model interfaces."""

from __future__ import annotations

import pytest
from superset_core.common.models import (
    Chart,
    CoreModel,
    Dashboard,
    Database,
    Dataset,
    get_session,
    KeyValue,
    Tag,
    User,
)
from superset_core.queries.models import Query, SavedQuery
from superset_core.semantic_layers.models import (
    SemanticLayerModel,
    SemanticViewModel,
)
from superset_core.tasks.models import Task, TaskSubscriber

ALL_MODELS = [
    CoreModel,
    Database,
    Dataset,
    Chart,
    Dashboard,
    User,
    Tag,
    KeyValue,
    Query,
    SavedQuery,
    Task,
    TaskSubscriber,
    SemanticLayerModel,
    SemanticViewModel,
]


@pytest.mark.parametrize("model", ALL_MODELS)
def test_model_interfaces_are_abstract(model: type[CoreModel]) -> None:
    # Every interface is a SQLAlchemy abstract model until the host maps it.
    assert model.__abstract__ is True


@pytest.mark.parametrize("model", ALL_MODELS)
def test_model_interfaces_extend_core_model(model: type[CoreModel]) -> None:
    assert issubclass(model, CoreModel)


def test_get_session_is_uninitialized() -> None:
    with pytest.raises(NotImplementedError):
        get_session()
