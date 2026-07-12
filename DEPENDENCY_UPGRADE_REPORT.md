# Dependency Upgrade Report: `apispec` 6.6.1 → 6.7.0

- **Dependency:** `apispec`
- **Current version:** `6.6.1`
- **Target version:** `6.7.0`
- **Base commit analyzed:** [`6a8619b`](https://github.com/ezkalan16/superset/commit/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1)

## Where the current version is pinned

- [`requirements/base.in#L43`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.in#L43) — constraint `apispec>=6.0.0,<6.7.0` (note: this bound explicitly excluded `6.7.0`, with a comment flagging a known unit-test break).
- [`requirements/base.txt#L11`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.txt#L11) — pinned `apispec==6.6.1`.
- [`requirements/development.txt#L35`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/development.txt#L35) — pinned `apispec==6.6.1`.

`apispec` is also pulled in transitively via `flask-appbuilder`, but Superset declares it directly for pinning.

## Changelog between 6.6.1 and 6.7.0

Source: [apispec CHANGELOG — 6.7.0 (2024-10-20)](https://github.com/marshmallow-code/apispec/blob/6.7.0/CHANGELOG.rst)

`6.7.0` is the release immediately following `6.6.1`; it contains exactly three entries:

- **Bug fix:** Fix handling of `fields.Dict()` with `values` unset ([issue #949](https://github.com/marshmallow-code/apispec/issues/949)). A bare `fields.Dict()` (no `values=`) now renders `additionalProperties: {}` instead of omitting `additionalProperties` entirely.
- **Other:** Officially support Python 3.13 ([PR #948](https://github.com/marshmallow-code/apispec/pull/948)).
- **Other:** Drop support for Python 3.8 ([PR #947](https://github.com/marshmallow-code/apispec/pull/947)).

The Python 3.8 drop is not relevant: Superset already requires Python `>=3.10` ([`pyproject.toml#L27`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/pyproject.toml#L27)).

## How this codebase uses `apispec`

Direct API surface used: the `APISpec(...)` constructor, `MarshmallowPlugin`, `spec.components.schema(name, schema=...)`, `spec.to_dict()`, and `apispec.exceptions.DuplicateComponentNameError`. None of these were removed, renamed, or changed in signature/return type in 6.7.0.

`APISpec` construction / OpenAPI generation sites:
- [`superset/cli/update.py#L83`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L83) (imports [L24-L25](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L24)) — `superset update-api-docs` regenerates `docs/static/resources/openapi.json`.
- [`superset/db_engine_specs/base.py#L2850`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2850) (imports [L43-L44](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L43)) — `parameters_json_schema()`.
- [`superset/db_engine_specs/gsheets.py#L342`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L342) (imports [L26-L27](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L26)).
- [`superset/db_engine_specs/snowflake.py#L426`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L426) (imports [L26-L27](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L26)).
- [`superset/db_engine_specs/databricks.py#L708`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L708) (imports [L23-L24](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L23)).
- [`superset/db_engine_specs/bigquery.py#L981`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L981) (imports [L29-L30](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L29)).
- [`superset/db_engine_specs/datastore.py#L459`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L459) (imports [L27-L28](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L27)).
- [`superset/db_engine_specs/duckdb.py#L183`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L183) (imports [L25-L26](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L25)).
- [`superset/temporary_cache/api.py#L57`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L57) — `add_apispec_components()`, uses `DuplicateComponentNameError` (imports [L22-L23](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L22)).

Marshmallow schemas rendered through `MarshmallowPlugin` that use a **bare `fields.Dict()` (no `values=`)** — the only fields affected by the 6.7.0 bug fix:
- [`superset/db_engine_specs/gsheets.py#L67`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67) — `catalog = fields.Dict()`.
- [`superset/db_engine_specs/bigquery.py#L213`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L213) — `query = fields.Dict(required=False)`.
- [`superset/db_engine_specs/datastore.py#L101`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L101) — `query = fields.Dict(required=False)`.

(The `query` fields in `base.py`, `clickhouse.py`, `couchbase.py`, `databend.py`, and `duckdb.py` use `values=fields.Raw()`, which already produced `additionalProperties: {}` on 6.6.1 and are therefore unaffected.)

---

## Impact Report

### Breaking changes

- **`fields.Dict()` with `values` unset now emits `additionalProperties: {}`** ([apispec #949](https://github.com/marshmallow-code/apispec/issues/949), CHANGELOG 6.7.0). This changes the default OpenAPI rendering of the bare-`Dict` fields listed above, which breaks tests that snapshot the exact generated schema. These MUST be fixed for the upgrade and have been updated in this PR:
  - [`tests/unit_tests/databases/api_test.py#L286`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/unit_tests/databases/api_test.py#L286) — GSheets `catalog` expected schema.
  - [`tests/integration_tests/databases/api_tests.py#L3519`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/databases/api_tests.py#L3519) — BigQuery `query` expected schema.
  - [`tests/integration_tests/databases/api_tests.py#L3600`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/databases/api_tests.py#L3600) — GSheets `catalog` expected schema.

  This is the "known issue" that the pre-existing comment on `requirements/base.in` referenced when it capped the version at `<6.7.0`.

### New deprecations

None. No API used by this codebase is deprecated in 6.7.0.

### Changes to existing functionality

- **Generated OpenAPI output changes at runtime.** The same `fields.Dict()` bug fix ([apispec #949](https://github.com/marshmallow-code/apispec/issues/949)) also alters the OpenAPI documents produced at runtime — the `GET /api/v1/_openapi` endpoint and the `superset update-api-docs` output ([`superset/cli/update.py#L83`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L83)) — as well as `parameters_json_schema()` output for the affected engine specs. Bare-`Dict` fields now include `additionalProperties: {}`. This is a documentation-only, spec-still-valid change; see `BEHAVIORAL_IMPACT_REPORT.md` for the assessment.

### New functionality that can be used in the codebase

None. Release 6.7.0 introduces no new features (only the `fields.Dict()` bug fix plus Python-version support changes).

---

## Migration steps applied in this PR

1. Bumped the pin/constraint to `6.7.0`:
   - `requirements/base.in`: `apispec>=6.0.0,<6.7.0` → `apispec>=6.0.0,<6.8.0` and removed the now-obsolete "known issue" comment.
   - `requirements/base.txt`: `apispec==6.6.1` → `apispec==6.7.0`.
   - `requirements/development.txt`: `apispec==6.6.1` → `apispec==6.7.0`.
2. Updated the three schema-snapshot test expectations (listed under **Breaking changes**) to include `additionalProperties: {}` for the affected bare-`Dict` fields.

## Verification

- `apispec==6.7.0` installed in a fresh venv; `pytest tests/unit_tests/databases/api_test.py::test_database_connection` and the `parameters_json_schema` unit tests pass.
- `ruff check` / `ruff format --check` pass on the changed files.
- The remaining unit-test failures observed locally (`tests/unit_tests/mcp_service/semantic_layer/tool/test_list_metrics.py` and `tests/unit_tests/db_engine_specs/test_bigquery.py::test_fetch_data_*`) reproduce identically on `apispec==6.6.1` and are therefore pre-existing and unrelated to this upgrade.
