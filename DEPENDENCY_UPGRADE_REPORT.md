<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# Dependency Upgrade Report: `apispec`

- **Dependency:** `apispec`
- **Current version:** `6.6.1`
- **Target version:** `6.7.0`
- **Manifests / lockfiles updated:**
  - `requirements/base.in` (`apispec>=6.0.0,<6.7.0` → `apispec>=6.0.0,<6.8.0`)
  - `requirements/base.txt` (`apispec==6.6.1` → `apispec==6.7.0`)
  - `requirements/development.txt` (`apispec==6.6.1` → `apispec==6.7.0`)

## Research sources

- **DeepWiki (primary):**
  - `marshmallow-code/apispec` is indexed. DeepWiki confirmed that the only functional change
    between 6.6.1 and 6.7.0 is the `MarshmallowPlugin` fix for `fields.Dict()` with `values` unset
    (now emits `additionalProperties: {}`), and that there are **no breaking API changes or new
    deprecations** in `MarshmallowPlugin` in this range.
  - `ezkalan16/superset` is **not indexed** in DeepWiki ("Repository not found"). All codebase
    findings below were verified directly against the current checkout at commit
    `6a8619bd4f643f634b3beb3cce1f902cd4ff80a1`.
- **Official sources:**
  - apispec `CHANGELOG.rst` (6.7.0, 2024-10-20): https://github.com/marshmallow-code/apispec/blob/6.7.0/CHANGELOG.rst
  - Source diff 6.6.1...6.7.0: https://github.com/marshmallow-code/apispec/compare/6.6.1...6.7.0
  - Fixed issue: https://github.com/marshmallow-code/apispec/issues/949

## Changelog summary (6.6.1 → 6.7.0)

From the official changelog, `6.7.0` contains exactly three changes:

- **Bug fix:** Fix handling of `fields.Dict()` with `values` unset (issue #949). A bare
  `fields.Dict()` now produces `additionalProperties: {}` in the generated OpenAPI schema instead
  of omitting `additionalProperties` entirely. (Diff: `src/apispec/ext/marshmallow/field_converter.py`
  `dict2properties`.)
- **Other:** Officially support Python 3.13 (PR #948).
- **Other:** Drop support for Python 3.8 (PR #947). Not relevant — Superset requires
  `requires-python = ">=3.10"` ([pyproject.toml#L27](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/pyproject.toml#L27)).

## How the codebase uses `apispec`

Direct API usage (verified in the current checkout):

- `from apispec import APISpec` — construct an `APISpec` and call `spec.components.schema(...)` then
  `spec.to_dict()` to render a marshmallow schema to an OpenAPI schema fragment.
- `from apispec.ext.marshmallow import MarshmallowPlugin` — the marshmallow plugin (sometimes with
  `schema_name_resolver=resolver`, and with `init_spec` / `converter.add_attribute_function`).
- `from apispec.exceptions import DuplicateComponentNameError` — suppressed when re-registering
  components.

Usage sites:

- [superset/cli/update.py#L24-L25](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L24-L25),
  used at [#L83-L98](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L83-L98) (`update_api_docs` regenerates `docs/static/resources/openapi.json`).
- [superset/db_engine_specs/base.py#L43-L44](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L43-L44),
  used at [#L2850-L2857](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2850-L2857) (`parameters_json_schema`).
- [superset/db_engine_specs/gsheets.py#L26-L27](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L26-L27),
  used at [#L342-L352](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L342-L352).
- [superset/db_engine_specs/duckdb.py#L25-L26](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L25-L26),
  used at [#L183-L190](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L183-L190).
- [superset/db_engine_specs/snowflake.py#L26-L27](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L26-L27),
  used at [#L425-L434](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L425-L434).
- [superset/db_engine_specs/datastore.py#L27-L28](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L27-L28),
  used at [#L459-L469](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L459-L469).
- [superset/db_engine_specs/bigquery.py#L29-L30](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L29-L30),
  used at [#L981-L991](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L981-L991).
- [superset/db_engine_specs/databricks.py#L23-L24](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L23-L24),
  used at [#L708-L715](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L708-L715).
- [superset/temporary_cache/api.py#L22-L23](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L22-L23),
  used at [#L57-L67](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L57-L67).

`apispec` is also consumed transitively via `flask-appbuilder`, which uses `MarshmallowPlugin` to
build the Swagger/OpenAPI spec for every REST API from its marshmallow schemas.

## Impact report

### Breaking changes

- **`fields.Dict()` with no `values` now emits `additionalProperties: {}`** (apispec #949 /
  [CHANGELOG 6.7.0](https://github.com/marshmallow-code/apispec/blob/6.7.0/CHANGELOG.rst),
  [`dict2properties` diff](https://github.com/marshmallow-code/apispec/compare/6.6.1...6.7.0)).
  This is a changed default in the OpenAPI output. It does not break runtime behavior, but it broke
  test fixtures that assert the exact generated schema, so it **must** be fixed for the upgrade.
  - Root cause in this codebase: the GSheets parameters schema declares a bare `catalog = fields.Dict()` at
    [superset/db_engine_specs/gsheets.py#L67](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67),
    which is rendered by `parameters_json_schema` at
    [#L342-L352](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L342-L352).
  - Fixtures updated to the new output (`{"type": "object", "additionalProperties": {}}`):
    - [tests/unit_tests/databases/api_test.py#L286](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/unit_tests/databases/api_test.py#L286) (`test_database_connection`)
    - [tests/integration_tests/databases/api_tests.py#L3600](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/databases/api_tests.py#L3600)
  - Note: `fields.Dict(keys=..., values=fields.Raw())` fields such as `BasicParametersSchema.query`
    ([base.py#L2663-L2666](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2663-L2666))
    are unaffected — they already produced `additionalProperties: {}` in 6.6.1 because `values` was set.

### New deprecations

None. No `MarshmallowPlugin`/`APISpec` API used by this codebase is deprecated in 6.7.0. The
`apispec.__version__` deprecation predates the current version (introduced in 6.5.0) and the codebase
does not reference it.

### Changes to existing functionality

None beyond the `fields.Dict()` output change already listed under **Breaking changes**.

### New functionality that can be used in the codebase

None. `6.7.0` adds only Python 3.13 support and a bug fix; it introduces no new `apispec` API that is
relevant to how this codebase uses the dependency.

## Migration steps applied

1. Bumped the version constraint in `requirements/base.in` from `<6.7.0` to `<6.8.0` and removed the
   stale comment that pinned it below `6.7.0`.
2. Bumped the pinned version to `6.7.0` in `requirements/base.txt` and `requirements/development.txt`.
3. Updated the two test fixtures that asserted the pre-6.7.0 GSheets `catalog` schema to expect
   `additionalProperties: {}`.

## Verification

- Installed `apispec==6.7.0` in a dev virtualenv.
- `tests/unit_tests/databases/api_test.py` passes (115 passed, 1 skipped), including the previously
  failing `test_database_connection`.
- The only apispec-caused failure across `tests/unit_tests/databases` and
  `tests/unit_tests/db_engine_specs` was `test_database_connection`; it now passes. The five
  `test_bigquery.py::test_fetch_data_*` failures are pre-existing and unrelated to apispec (they fail
  identically on `apispec==6.6.1`; they are caused by an `AsyncMock`/`MagicMock` interaction in the
  test environment).
