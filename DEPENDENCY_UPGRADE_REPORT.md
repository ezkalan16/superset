# Dependency Upgrade Impact Report: `apispec`

- **Dependency:** `apispec` (with the `[yaml]`/`ext.marshmallow` extras, pulled in directly and via `flask-appbuilder`)
- **Current version:** `6.6.1`
- **Target version:** `6.7.0`
- **Base commit for links:** `6a8619bd4f643f634b3beb3cce1f902cd4ff80a1`

## Version pin locations

- [`requirements/base.in`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.in#L45) — constraint `apispec>=6.0.0,<6.7.0` (bumped to `<6.8.0`)
- [`requirements/base.txt`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.txt#L11) — pinned `apispec==6.6.1`
- [`requirements/development.txt`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/development.txt#L35) — pinned `apispec==6.6.1`

## Changelog reviewed (6.6.1 → 6.7.0)

Only one release sits between the current and target versions. From the [official changelog](https://github.com/marshmallow-code/apispec/blob/6.7.0/CHANGELOG.rst):

> **6.7.0 (2024-10-20)**
> - *Bug fixes:* Fix handling of `fields.Dict()` with `values` unset ([#949](https://github.com/marshmallow-code/apispec/issues/949)).
> - *Other changes:* Officially support Python 3.13 ([#948](https://github.com/marshmallow-code/apispec/pull/948)). Drop support for Python 3.8 ([#947](https://github.com/marshmallow-code/apispec/pull/947)).

There are no public API removals, renames, or signature changes in this release. `flask-appbuilder==5.2.2` (which also depends on apispec) declares `apispec[yaml] <7,>=6.0.0`, so it is fully compatible with `6.7.0`.

## How the codebase uses `apispec`

Direct API surface used by Superset (all unchanged in 6.7.0):

- `from apispec import APISpec` and `from apispec.ext.marshmallow import MarshmallowPlugin` — used to build an OpenAPI spec object:
  - [`superset/cli/update.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L24-L25) / [L83](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L83)
  - [`superset/db_engine_specs/base.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L43-L44) / [L2850](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2850) (`parameters_json_schema()`)
  - [`superset/db_engine_specs/bigquery.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L29-L30)
  - [`superset/db_engine_specs/databricks.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L23-L24)
  - [`superset/db_engine_specs/datastore.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L27-L28)
  - [`superset/db_engine_specs/duckdb.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L25-L26)
  - [`superset/db_engine_specs/gsheets.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L26-L27)
  - [`superset/db_engine_specs/snowflake.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L26-L27)
- `api_spec.components.schema(...)` and `from apispec.exceptions import DuplicateComponentNameError` — [`superset/temporary_cache/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L22-L23) / [L57-L67](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L57-L67)

Flask-AppBuilder also drives apispec transparently: every `ModelRestApi` renders its Marshmallow schemas into the OpenAPI document served at `/api/v1/_openapi` and written by the `superset update-api-docs` CLI command. The `apispec_parameter_schemas = {...}` attributes found across the API modules (e.g. `superset/charts/api.py`, `superset/dashboards/api.py`, ...) are Flask-AppBuilder configuration and are not affected by this upgrade.

The one behavioral change (`fields.Dict()` with `values` unset) is only relevant where the codebase declares a **bare** `fields.Dict()` (no `values=`) on a Marshmallow schema that apispec serializes:

- [`superset/db_engine_specs/gsheets.py#L67`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67) — `catalog = fields.Dict()`
- [`superset/db_engine_specs/bigquery.py#L213`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L213) — `query = fields.Dict(required=False)`
- [`superset/db_engine_specs/datastore.py#L101`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L101) — `query = fields.Dict(required=False)`
- [`superset/views/base_api.py#L70`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/base_api.py#L70) — `extra = fields.Dict(...)` (`RelatedResponseSchema`, part of the main OpenAPI doc)
- [`superset/semantic_layers/schemas.py#L29`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/semantic_layers/schemas.py#L29), [L36](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/semantic_layers/schemas.py#L36), [L43](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/semantic_layers/schemas.py#L43) — `configuration = fields.Dict(...)`
- [`superset/sqllab/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L115) — `extra`, `data`, `columns`, `extra_json`, etc. (L115, L120-L123, L142)
- [`superset/reports/schemas.py#L425`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/schemas.py#L425) — `extra = fields.Dict(dump_default=None)`

`fields.Dict(..., values=fields.Raw())` usages (e.g. `BasicParametersSchema.query` in [`superset/db_engine_specs/base.py#L2663`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2663) and the clickhouse/couchbase/databend/duckdb specs) already emitted `additionalProperties: {}` in 6.6.1 and are **not** changed by this upgrade.

---

## Impact Report

### Breaking changes

**None.** apispec 6.7.0 removes/renames no public API and changes no signatures. Every symbol Superset imports (`APISpec`, `MarshmallowPlugin`, `APISpec.components.schema`, `apispec.exceptions.DuplicateComponentNameError`, and the `APISpec(...)` constructor keyword arguments) is unchanged. The dropped Python 3.8 support is irrelevant because Superset already requires Python `>=3.9`.

### New deprecations

**None.** No API used by this codebase is deprecated in 6.7.0.

### Changes to existing functionality

- **`fields.Dict()` with `values` unset now renders `additionalProperties: {}` in the generated OpenAPI/JSON schema** (previously the key was omitted, leaving just `{"type": "object"}`). Source: apispec [CHANGELOG 6.7.0](https://github.com/marshmallow-code/apispec/blob/6.7.0/CHANGELOG.rst) / [issue #949](https://github.com/marshmallow-code/apispec/issues/949). This is a spec-generation output change only (it does not affect request validation or runtime behavior). It affects the bare `fields.Dict()` declarations listed above, most visibly:
  - Database connection parameters served by `/api/v1/database/available` and `parameters_json_schema()` — [`gsheets.py#L67`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67), [`bigquery.py#L213`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L213), [`datastore.py#L101`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L101).
  - The main `/api/v1/_openapi` document — [`views/base_api.py#L70`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/base_api.py#L70) and the sqllab/reports/semantic-layer schemas above.

  See `BEHAVIORAL_IMPACT_REPORT.md` for the full behavioral assessment. In short: the emitted schema stays semantically equivalent (`additionalProperties: {}` means "any additional properties allowed", which is the OpenAPI default), remains a valid OpenAPI 3.0 document (`test_open_api_spec` still passes), and only required updating hard-coded expected values in three test fixtures.

### New functionality that can be used in the codebase

**None.** The only non-fix items in 6.7.0 are Python 3.13 support and dropping Python 3.8 — neither introduces a new apispec API for Superset to adopt.

---

## Migration steps applied

1. Bumped the constraint in `requirements/base.in` from `apispec>=6.0.0,<6.7.0` to `apispec>=6.0.0,<6.8.0` (and removed the stale "known issue with 6.7.0 breaking a unit test" comment).
2. Pinned `apispec==6.7.0` in `requirements/base.txt` and `requirements/development.txt`.
3. Updated the three test fixtures that hard-code the generated schema for bare `fields.Dict()` fields to expect `additionalProperties: {}`:
   - `tests/unit_tests/databases/api_test.py` — gsheets `catalog`.
   - `tests/integration_tests/databases/api_tests.py` — bigquery `query` and gsheets `catalog`.
4. Verified `tests/unit_tests/databases/api_test.py` and `tests/unit_tests/db_engine_specs/` pass on 6.7.0. (The `test_bigquery.py::test_fetch_data_*` failures are pre-existing on 6.6.1 and unrelated to apispec — they stem from `AsyncMock` in the test environment.)
