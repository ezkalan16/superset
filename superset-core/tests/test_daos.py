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

"""Unit tests for the abstract DAO interfaces."""

from __future__ import annotations

from typing import Any

import pytest
from superset_core.common.daos import (
    BaseDAO,
    ChartDAO,
    DashboardDAO,
    DatabaseDAO,
    DatasetDAO,
    KeyValueDAO,
    TagDAO,
    UserDAO,
)
from superset_core.queries.daos import QueryDAO, SavedQueryDAO
from superset_core.tasks.daos import TaskDAO

ALL_DAOS = [
    DatasetDAO,
    DatabaseDAO,
    ChartDAO,
    DashboardDAO,
    UserDAO,
    TagDAO,
    KeyValueDAO,
    QueryDAO,
    SavedQueryDAO,
    TaskDAO,
]

UUID_DAOS = [DatasetDAO, DatabaseDAO, ChartDAO, DashboardDAO, TaskDAO]


def test_base_dao_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseDAO()


@pytest.mark.parametrize("dao", ALL_DAOS)
def test_dao_class_variable_defaults(dao: type[BaseDAO[Any]]) -> None:
    # Host implementations override these; the stubs must ship neutral defaults.
    assert dao.model_cls is None
    assert dao.base_filter is None
    assert dao.id_column_name == "id"


@pytest.mark.parametrize("dao", UUID_DAOS)
def test_uuid_daos_expose_uuid_column(dao: type[BaseDAO[Any]]) -> None:
    assert dao.uuid_column_name == "uuid"


@pytest.mark.parametrize("dao", ALL_DAOS)
def test_dao_stubs_cannot_be_instantiated(dao: type[BaseDAO[Any]]) -> None:
    # Abstract CRUD methods are still unimplemented in the stubs.
    with pytest.raises(TypeError):
        dao()


def test_task_dao_declares_find_by_task_key() -> None:
    assert getattr(TaskDAO.find_by_task_key, "__isabstractmethod__", False)
