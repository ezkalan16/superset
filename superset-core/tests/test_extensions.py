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

"""Unit tests for ``superset_core.extensions`` constants and types."""

from __future__ import annotations

import re

import pytest
from pydantic import ValidationError
from superset_core.extensions.constants import (
    DISPLAY_NAME_PATTERN,
    PUBLISHER_PATTERN,
    TECHNICAL_NAME_PATTERN,
    VERSION_PATTERN,
)
from superset_core.extensions.types import (
    ExtensionConfig,
    ExtensionConfigBackend,
    Manifest,
    ManifestBackend,
    ManifestFrontend,
)


@pytest.mark.parametrize(
    "value",
    ["acme", "acme-tools", "a", "a1", "acme-tools-2"],
)
def test_publisher_pattern_accepts_valid_names(value: str) -> None:
    assert re.match(PUBLISHER_PATTERN, value)
    assert re.match(TECHNICAL_NAME_PATTERN, value)


@pytest.mark.parametrize(
    "value",
    ["Acme", "1acme", "acme-", "acme--tools", "-acme", "acme_tools"],
)
def test_publisher_pattern_rejects_invalid_names(value: str) -> None:
    assert re.match(PUBLISHER_PATTERN, value) is None


@pytest.mark.parametrize("value", ["Acme Tools", "My_Extension", "A.b-c", "Name1"])
def test_display_name_pattern_accepts_valid_names(value: str) -> None:
    assert re.match(DISPLAY_NAME_PATTERN, value)


@pytest.mark.parametrize("value", ["1name", " leading", "-name", "_name"])
def test_display_name_pattern_rejects_invalid_names(value: str) -> None:
    assert re.match(DISPLAY_NAME_PATTERN, value) is None


@pytest.mark.parametrize("value", ["0.0.0", "1.2.3", "10.20.30"])
def test_version_pattern_accepts_semver(value: str) -> None:
    assert re.match(VERSION_PATTERN, value)


@pytest.mark.parametrize("value", ["1.0", "1.0.0.0", "v1.0.0", "1.0.x"])
def test_version_pattern_rejects_non_semver(value: str) -> None:
    assert re.match(VERSION_PATTERN, value) is None


def test_extension_config_minimal_defaults() -> None:
    config = ExtensionConfig(
        publisher="acme",
        name="tools",
        displayName="Acme Tools",
    )

    assert config.version == "0.0.0"
    assert config.license is None
    assert config.description is None
    assert config.dependencies == []
    assert config.permissions == []
    assert config.backend is None


def test_extension_config_with_backend() -> None:
    config = ExtensionConfig(
        publisher="acme",
        name="tools",
        displayName="Acme Tools",
        backend=ExtensionConfigBackend(files=["backend/*.py"]),
    )

    assert config.backend is not None
    assert config.backend.files == ["backend/*.py"]


def test_extension_config_default_backend_files_is_empty() -> None:
    assert ExtensionConfigBackend().files == []


@pytest.mark.parametrize("bad_publisher", ["Acme", "1acme", "acme--tools"])
def test_extension_config_rejects_invalid_publisher(bad_publisher: str) -> None:
    with pytest.raises(ValidationError):
        ExtensionConfig(
            publisher=bad_publisher,
            name="tools",
            displayName="Acme Tools",
        )


def test_extension_config_rejects_invalid_version() -> None:
    with pytest.raises(ValidationError):
        ExtensionConfig(
            publisher="acme",
            name="tools",
            displayName="Acme Tools",
            version="1.0",
        )


def test_manifest_requires_id() -> None:
    with pytest.raises(ValidationError):
        Manifest(publisher="acme", name="tools", displayName="Acme Tools")


def test_manifest_full() -> None:
    manifest = Manifest(
        id="acme.tools",
        publisher="acme",
        name="tools",
        displayName="Acme Tools",
        frontend=ManifestFrontend(
            remoteEntry="dist/remoteEntry.js",
            moduleFederationName="acme_tools",
        ),
        backend=ManifestBackend(entrypoint="backend.main"),
    )

    assert manifest.id == "acme.tools"
    assert manifest.frontend is not None
    assert manifest.frontend.remoteEntry == "dist/remoteEntry.js"
    assert manifest.backend is not None
    assert manifest.backend.entrypoint == "backend.main"


def test_manifest_frontend_requires_all_fields() -> None:
    with pytest.raises(ValidationError):
        ManifestFrontend(remoteEntry="dist/remoteEntry.js")
