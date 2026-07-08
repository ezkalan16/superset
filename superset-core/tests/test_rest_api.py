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

"""Unit tests for ``superset_core.rest_api.api``."""

from __future__ import annotations

from flask_appbuilder.api import BaseApi
from superset_core.rest_api.api import RestApi


def test_rest_api_extends_base_api() -> None:
    assert issubclass(RestApi, BaseApi)


def test_rest_api_enables_browser_login() -> None:
    assert RestApi.allow_browser_login is True
