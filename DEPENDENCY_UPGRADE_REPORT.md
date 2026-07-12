# Dependency Upgrade Report: `apispec`

- **Dependency:** `apispec`
- **Current version:** `6.6.1`
- **Target version:** `6.7.0`
- **Repository:** https://github.com/ezkalan16/superset
- **Base commit for links:** `6a8619bd4f643f634b3beb3cce1f902cd4ff80a1`

## Current version and where it is pinned

`apispec` is both a direct dependency (declared in `requirements/base.in`) and a
transitive dependency (of `flask-appbuilder`). The current resolved version is
`6.6.1`:

- Constraint (before upgrade): `apispec>=6.0.0,<6.7.0` — [requirements/base.in#L45](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.in#L45)
- Pinned in [requirements/base.txt#L11](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.txt#L11)
- Pinned in [requirements/development.txt#L35](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/development.txt#L35)

The existing constraint `<6.7.0` explicitly excluded `6.7.0`, with a code comment
noting a "Known issue with 6.7.0 breaking a unit test" —
[requirements/base.in#L43-L45](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.in#L43).
That known issue is the `fields.Dict()` behavior change described below, and it is
fixed by this upgrade.

## How the codebase uses `apispec`

Direct API surface used:

- `APISpec` constructor and `MarshmallowPlugin` — used to render marshmallow
  schemas into OpenAPI component schemas:
  - [superset/cli/update.py#L24-L25, L83-L88](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L83) (full OpenAPI spec generation)
  - [superset/db_engine_specs/base.py#L43-L44, L2850-L2854](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2850) (`parameters_json_schema`)
  - [superset/db_engine_specs/bigquery.py#L29-L30, L981](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L981)
  - [superset/db_engine_specs/gsheets.py#L26-L27, L342](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L342)
  - [superset/db_engine_specs/datastore.py#L27-L28, L459](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L459)
  - [superset/db_engine_specs/databricks.py#L23-L24, L708](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L708)
  - [superset/db_engine_specs/duckdb.py#L25-L26, L183](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L183)
  - [superset/db_engine_specs/snowflake.py#L26-L27, L425-L426](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L425)
- `apispec.exceptions.DuplicateComponentNameError` —
  [superset/temporary_cache/api.py#L22-L23, L57-L58](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L57)

Indirect usage: Flask-AppBuilder drives most OpenAPI generation for the REST API
resources (the many `apispec_parameter_schemas = {...}` attributes on `*RestApi`
classes and `MarshmallowPlugin`'s conversion of every marshmallow schema in
`superset/**/schemas.py`).

## Changelog reviewed

Only one release sits between `6.6.1` and `6.7.0`:

**6.7.0 (2024-10-20)** — source: https://github.com/marshmallow-code/apispec/blob/6.7.0/CHANGELOG.rst

- Bug fix: "Fix handling of `fields.Dict()` with `values` unset" (issue
  [#949](https://github.com/marshmallow-code/apispec/issues/949), PR
  [#950](https://github.com/marshmallow-code/apispec/pull/950)). A
  `marshmallow.fields.Dict` with no `values` argument now renders
  `additionalProperties: {}` instead of omitting `additionalProperties`.
- Other: Officially support Python 3.13; drop support for Python 3.8.

No API was removed, renamed, or had its signature changed. `APISpec`,
`MarshmallowPlugin`, and `DuplicateComponentNameError` are unchanged.

---

## Impact Report

### Breaking changes

- **`fields.Dict()` without `values` now emits `additionalProperties: {}`**
  (issue [#949](https://github.com/marshmallow-code/apispec/issues/949) / PR
  [#950](https://github.com/marshmallow-code/apispec/pull/950)). This changes the
  OpenAPI output for db-engine-spec parameter schemas that declare a `Dict` field
  without `values`, and breaks the existing test assertions that hard-code the old
  output. These MUST be fixed for the upgrade (and are fixed in this PR). Affected
  schema fields and the tests that assert their rendered output:
  - `bigquery` `query = fields.Dict(required=False)` — [superset/db_engine_specs/bigquery.py#L213](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L213); asserted at [tests/integration_tests/databases/api_tests.py#L3519](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/databases/api_tests.py#L3519)
  - `gsheets` `catalog = fields.Dict()` — [superset/db_engine_specs/gsheets.py#L67](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67); asserted at [tests/unit_tests/databases/api_test.py#L286](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/unit_tests/databases/api_test.py#L286) and [tests/integration_tests/databases/api_tests.py#L3600](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/databases/api_tests.py#L3600)
  - `datastore` `query = fields.Dict(required=False)` — [superset/db_engine_specs/datastore.py#L101](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L101) (rendered output changes, but no test asserts its full schema, so no test edit was required)

  Note: `Dict` fields that already pass `values=fields.Raw()` (e.g.
  [base.py#L2663](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2663),
  clickhouse, couchbase, databend, duckdb) already emitted `additionalProperties: {}`
  in `6.6.1` and are unaffected.

- **Dropped support for Python 3.8.** Not applicable — Superset requires
  `>=3.10` ([pyproject.toml#L27](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/pyproject.toml#L27)), so this has no impact.

### New deprecations

None. `6.7.0` introduces no deprecations. (The `apispec.__version__` deprecation
landed in `6.5.0`, before the current `6.6.1`, and the codebase does not reference
`apispec.__version__`.)

### Changes to existing functionality

- **Generated OpenAPI/Swagger spec now includes `additionalProperties: {}` for
  every `fields.Dict()` declared without `values`.** Beyond the db-engine-spec
  fields listed under "Breaking changes", this affects the rendered OpenAPI schema
  for the many marshmallow schemas across the REST API (e.g.
  [superset/dashboards/schemas.py](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L190),
  [superset/charts/schemas.py](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L1755),
  [superset/databases/schemas.py](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L797),
  [superset/datasets/schemas.py](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/schemas.py#L228),
  [superset/explore/schemas.py](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L29),
  [superset/sqllab/schemas.py](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L142)).
  Source: issue [#949](https://github.com/marshmallow-code/apispec/issues/949).
  This is documentation/spec-output only (marshmallow, not the OpenAPI spec,
  performs request validation), so it does not change API request/response
  behavior. See `BEHAVIORAL_IMPACT_REPORT.md` for the detailed assessment.

### New functionality that can be used in the codebase

None. `6.7.0` adds only Python 3.13 support and the `Dict` bug fix; it introduces
no new public API relevant to how this codebase uses `apispec`.

---

## Migration steps applied

1. Relaxed the constraint in `requirements/base.in` from `apispec>=6.0.0,<6.7.0`
   to `apispec>=6.7.0,<6.8.0` and removed the stale "known issue" comment.
2. Bumped the pin `apispec==6.6.1` → `apispec==6.7.0` in `requirements/base.txt`
   and `requirements/development.txt`.
3. Updated the three test assertions that hard-code the pre-`6.7.0` OpenAPI output
   for `Dict`-without-`values` fields to include `additionalProperties: {}`:
   - `tests/unit_tests/databases/api_test.py` (gsheets `catalog`)
   - `tests/integration_tests/databases/api_tests.py` (bigquery `query`, gsheets `catalog`)
