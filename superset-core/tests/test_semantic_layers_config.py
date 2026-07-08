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

"""Unit tests for ``superset_core.semantic_layers.config``."""

from __future__ import annotations

from pydantic import BaseModel, Field
from superset_core.semantic_layers.config import (
    build_configuration_schema,
    check_dependencies,
)


class SampleConfig(BaseModel):
    """Config whose field order intentionally differs from alphabetical order."""

    zeta: str = Field(default="", json_schema_extra={"x-dynamic": True})
    alpha: str = ""
    beta: str = ""


def test_build_configuration_schema_preserves_field_order() -> None:
    schema = build_configuration_schema(SampleConfig)

    # Pydantic sorts alphabetically; the helper must restore declaration order.
    assert list(schema["properties"].keys()) == ["zeta", "alpha", "beta"]


def test_build_configuration_schema_sets_empty_enum_when_no_configuration() -> None:
    schema = build_configuration_schema(SampleConfig, configuration=None)

    # Only the ``x-dynamic`` property gets an empty enum.
    assert schema["properties"]["zeta"]["enum"] == []
    assert "enum" not in schema["properties"]["alpha"]
    assert "enum" not in schema["properties"]["beta"]


def test_build_configuration_schema_skips_empty_enum_with_configuration() -> None:
    schema = build_configuration_schema(SampleConfig, configuration=SampleConfig())

    # With a configuration provided, dynamic props are left untouched.
    assert "enum" not in schema["properties"]["zeta"]


def test_build_configuration_schema_respects_field_alias() -> None:
    class AliasConfig(BaseModel):
        internal_name: str = Field(default="", alias="externalName")

    schema = build_configuration_schema(AliasConfig)

    assert "externalName" in schema["properties"]


def test_check_dependencies_all_satisfied() -> None:
    config = SampleConfig(alpha="value", beta="value")
    prop_schema = {"x-dependsOn": ["alpha", "beta"]}

    assert check_dependencies(prop_schema, config) is True


def test_check_dependencies_missing_dependency_value() -> None:
    config = SampleConfig(alpha="value", beta="")
    prop_schema = {"x-dependsOn": ["alpha", "beta"]}

    assert check_dependencies(prop_schema, config) is False


def test_check_dependencies_no_dependencies_is_satisfied() -> None:
    # An empty (or absent) dependency list means there is nothing to satisfy.
    assert check_dependencies({}, SampleConfig()) is True
    assert check_dependencies({"x-dependsOn": []}, SampleConfig()) is True


def test_check_dependencies_unknown_attribute_is_falsy() -> None:
    prop_schema = {"x-dependsOn": ["does_not_exist"]}

    assert check_dependencies(prop_schema, SampleConfig()) is False
