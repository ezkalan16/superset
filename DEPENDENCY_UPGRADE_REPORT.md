# Dependency Upgrade Impact Report: `apispec`

- **Dependency:** `apispec`
- **Current version:** `6.6.1`
- **Target version:** `6.7.0`
- **Requested via:** https://github.com/ezkalan16/superset/issues/7

## Where the current version is pinned

- `requirements/base.in` — `apispec>=6.0.0,<6.7.0` (upper bound explicitly excluded 6.7.0)
- `requirements/base.txt` — `apispec==6.6.1` (pip-compiled lockfile)
- `requirements/development.txt` — `apispec==6.6.1` (pip-compiled lockfile)

`apispec` is also a transitive dependency of `flask-appbuilder` (5.2.2), which requires
`apispec[yaml]>=6.0.0,<7`; `6.7.0` satisfies that constraint. Its only runtime dependency
(`packaging`, plus `PyYAML` via the `yaml` extra) is unchanged between 6.6.1 and 6.7.0.

## How the codebase uses `apispec`

The codebase uses a small, stable surface of the `apispec` API:

- `APISpec(...)` constructor with `title`, `version`, `openapi_version`, `plugins`,
  and optionally `info`/`servers`.
- `apispec.ext.marshmallow.MarshmallowPlugin` (optionally with `schema_name_resolver`).
- `spec.components.schema(name, schema=...)` and `spec.to_dict()`.
- `apispec.exceptions.DuplicateComponentNameError`.

Direct usage sites (commit `6a8619bd4f643f634b3beb3cce1f902cd4ff80a1`):

- [`superset/cli/update.py:24`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L24-L25), [`:83`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L83-L90) — generates the full `docs/static/resources/openapi.json`.
- [`superset/temporary_cache/api.py:22`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L22-L23), [`:57`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L57-L67) — `add_apispec_components` / `DuplicateComponentNameError`.
- `db_engine_specs.*.parameters_json_schema()` builds an `APISpec` + `MarshmallowPlugin` and calls `spec.components.schema(...)`:
  - [`superset/db_engine_specs/base.py:43`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L43-L44), [`:2850`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2850-L2857)
  - [`superset/db_engine_specs/bigquery.py:29`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L29-L30), [`:981`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L981-L988)
  - [`superset/db_engine_specs/snowflake.py:26`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L26-L27), [`:426`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L426)
  - [`superset/db_engine_specs/databricks.py:23`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L23-L24), [`:708`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L708)
  - [`superset/db_engine_specs/gsheets.py:26`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L26-L27), [`:342`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L342)
  - [`superset/db_engine_specs/datastore.py:27`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L27-L28), [`:459`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L459)
  - [`superset/db_engine_specs/duckdb.py:25`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L25-L26), [`:183`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L183)

(The many `apispec_parameter_schemas = {...}` attributes on the REST API classes are a
Flask-AppBuilder feature, not a direct `apispec` API; they are unaffected by this bump.)

## Changelog reviewed

Only one release sits between the current and target version.

**`apispec` 6.7.0 (2024-10-20)** — https://github.com/marshmallow-code/apispec/blob/master/CHANGELOG.rst

- Bug fix: *Fix handling of `fields.Dict()` with `values` unset* (issue #949).
- Other: Officially support Python 3.13 (PR #948).
- Other: Drop support for Python 3.8 (PR #947).

---

## Impact Report

### Breaking changes

- **`fields.Dict()` without a value type now emits `"additionalProperties": {}`.**
  Source: `apispec` 6.7.0 — "Fix handling of `fields.Dict()` with `values` unset" (issue #949).
  In 6.6.1 a marshmallow `fields.Dict()` declared without a `values` argument produced no
  `additionalProperties` key; in 6.7.0 it produces `"additionalProperties": {}`. This changes
  the schema that `db_engine_specs.*.parameters_json_schema()` returns for engines whose
  parameter schema has a bare `fields.Dict()`, and it broke the pinned build's unit test
  (`tests/unit_tests/databases/api_test.py::test_database_connection`) — which is exactly the
  "known issue" the `<6.7.0` cap in `requirements/base.in` referenced.
  Affected declarations (bare `fields.Dict()` in engine parameter schemas):
  - [`superset/db_engine_specs/gsheets.py:67`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67) — `catalog = fields.Dict()`
  - [`superset/db_engine_specs/bigquery.py:213`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L213) — `query = fields.Dict(required=False)`
  - [`superset/db_engine_specs/datastore.py:101`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L101) — `query = fields.Dict(required=False)`

  Affected test (fixed in this PR):
  - [`tests/unit_tests/databases/api_test.py:286`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/unit_tests/databases/api_test.py#L286) — the expected gsheets `catalog` schema is now `{"type": "object", "additionalProperties": {}}`.

  **Fix applied:** no production code change is required (the new output is the correct
  OpenAPI representation of an untyped dict); only the test expectation was updated to match.
  `fields.Dict(keys=..., values=fields.Raw())` fields (e.g. the `query` field in
  `BasicParametersSchema`) were already emitting `additionalProperties: {}` on 6.6.1 and are
  unaffected.

### New deprecations

None. `apispec` 6.7.0 introduces no deprecations affecting the APIs this codebase uses.

### Changes to existing functionality

- **Broader OpenAPI output drift from the same `fields.Dict()` fix.**
  Source: `apispec` 6.7.0 (issue #949). Beyond the single unit test above, the change also
  alters the generated global OpenAPI document (runtime `GET /api/v1/_openapi`, the
  `db_engine_specs` connection schemas, and the checked-in
  `docs/static/resources/openapi.json` produced by `superset update-api-docs`). Every
  marshmallow schema field declared as a bare `fields.Dict()` will now render
  `"additionalProperties": {}`. These are exposed via `cli/update.py`
  ([`superset/cli/update.py:83`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L83-L98)) and appear across many schemas, e.g.:
  - [`superset/dashboards/schemas.py:190`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L190)
  - [`superset/charts/schemas.py:1755`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L1755)
  - [`superset/databases/schemas.py:850`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L850)
  - [`superset/datasets/schemas.py:228`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/schemas.py#L228)

  This is a documentation/response-shape change, not a runtime failure. It is assessed for
  human review in `BEHAVIORAL_IMPACT_REPORT.md`.

- **Dropped Python 3.8 support (PR #947); added Python 3.13 support (PR #948).**
  Source: `apispec` 6.7.0. No impact: the project requires `python >=3.10`
  ([`pyproject.toml:27`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/pyproject.toml#L27)).

### New functionality that can be used in the codebase

None. `apispec` 6.7.0 adds no new API surface relevant to this codebase (its only
non-bugfix changes are Python-version support changes).

---

## Migration steps applied

1. `requirements/base.in`: `apispec>=6.0.0,<6.7.0` → `apispec>=6.7.0,<6.8.0` (removed the
   stale "6.7.0 breaks a unit test" comment now that the test is fixed).
2. `requirements/base.txt`: `apispec==6.6.1` → `apispec==6.7.0`.
3. `requirements/development.txt`: `apispec==6.6.1` → `apispec==6.7.0`.
4. `tests/unit_tests/databases/api_test.py`: updated the expected gsheets `catalog`
   parameter schema to `{"type": "object", "additionalProperties": {}}` to match the
   corrected 6.7.0 output.

### Verification

- `pip check` clean; `flask-appbuilder` 5.2.2 constraint (`apispec<7,>=6.0.0`) satisfied.
- `tests/unit_tests/db_engine_specs/` and `tests/unit_tests/databases/api_test.py::test_database_connection`
  pass on `apispec==6.7.0`. The only remaining unit-test failures on this branch
  (`test_list_metrics.*`, `bigquery.test_fetch_data_*`) are pre-existing and reproduce on
  `apispec==6.6.1`; they are unrelated to this upgrade.
