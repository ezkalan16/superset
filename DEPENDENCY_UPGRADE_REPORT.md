# Dependency Upgrade Impact Report: `apispec`

- **Dependency:** `apispec`
- **Current version:** `6.6.1`
- **Target version:** `6.7.0`
- **Analyzed commit:** `6a8619bd4f643f634b3beb3cce1f902cd4ff80a1`
- **Requested via:** [issue #18](https://github.com/ezkalan16/superset/issues/18)

## Research sources

- **DeepWiki (primary):** Queried `marshmallow-code/apispec` (confirmed the only functional
  change in 6.7.0 is the `fields.Dict()` `additionalProperties` fix; no breaking changes or
  deprecations to `APISpec`/`MarshmallowPlugin`). Queried `apache/superset` (upstream) to map
  apispec usage sites. The fork `ezkalan16/superset` is **not indexed on DeepWiki**, so every
  usage site below was verified directly against the current checkout at the commit above.
- **Official changelog:** https://github.com/marshmallow-code/apispec/blob/6.7.0/CHANGELOG.rst
  and the `6.6.1...6.7.0` diff.

## Changelog summary (6.6.1 → 6.7.0)

The only release in this range is **6.7.0 (2024-10-20)**:

- **Bug fix:** Fix handling of `fields.Dict()` with `values` unset ([apispec #949](https://github.com/marshmallow-code/apispec/issues/949)).
  `dict2properties` now emits `"additionalProperties": {}` when the Dict field has no `value_field`,
  whereas 6.6.1 emitted no `additionalProperties` key at all.
- **Other:** Officially support Python 3.13; drop support for Python 3.8.

No changes to the public API surface used by this codebase (`APISpec`, `MarshmallowPlugin`,
`apispec.exceptions.DuplicateComponentNameError`, `spec.components.schema(...)`, `spec.to_dict()`).

## apispec usage in this codebase

Direct API usage (`APISpec` / `MarshmallowPlugin` / `DuplicateComponentNameError`):

- `superset/db_engine_specs/base.py` — imports + `APISpec(...)` in `parameters_json_schema`
  ([L43-L44](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L43-L44), [L2850](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2850))
- `superset/db_engine_specs/bigquery.py` ([L29-L30](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L29-L30), [L981](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L981))
- `superset/db_engine_specs/databricks.py` ([L23-L24](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L23-L24), [L708](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L708))
- `superset/db_engine_specs/datastore.py` ([L27-L28](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L27-L28), [L459](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L459))
- `superset/db_engine_specs/duckdb.py` ([L25-L26](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L25-L26), [L183](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L183))
- `superset/db_engine_specs/gsheets.py` ([L26-L27](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L26-L27), [L342](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L342))
- `superset/db_engine_specs/snowflake.py` ([L26-L27](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L26-L27), [L426](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L426))
- `superset/cli/update.py` — imports + `APISpec(...)` for `openapi.json` generation ([L24-L25](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L24-L25), [L83](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L83))
- `superset/temporary_cache/api.py` — `APISpec` type hint + `DuplicateComponentNameError` ([L22-L23](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L22-L23), [L57-L67](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L57-L67))

Flask-AppBuilder also uses apispec transitively to build the app-wide Swagger spec from every
`ModelRestApi` schema (the many `apispec_parameter_schemas = {...}` sites and all marshmallow
schemas in `superset/**/schemas.py`).

The `fields.Dict()`-without-`values` fields that are affected by the behavioral change include,
among others:

- `superset/db_engine_specs/bigquery.py` `query = fields.Dict(required=False)` ([L213](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L213))
- `superset/db_engine_specs/datastore.py` `query = fields.Dict(required=False)` ([L101](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L101))
- `superset/db_engine_specs/gsheets.py` `catalog = fields.Dict()` ([L67](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67))

## Impact report

### Breaking changes

**None.**

- The public apispec API used by the codebase (`APISpec(...)`, `MarshmallowPlugin(...)`,
  `spec.components.schema(...)`, `spec.to_dict()`, `DuplicateComponentNameError`) is unchanged in
  6.7.0.
- "Drop support for Python 3.8" does not affect this codebase — it requires `python >= 3.10`
  ([pyproject.toml L27](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/pyproject.toml#L27)).

### New deprecations

**None.** apispec 6.7.0 introduces no deprecations affecting APIs used here.

### Changes to existing functionality

- **`fields.Dict()` without `values` now renders `"additionalProperties": {}`** in generated
  OpenAPI (apispec [#949](https://github.com/marshmallow-code/apispec/issues/949)). Previously such
  a field rendered as `{"type": "object"}` with no `additionalProperties` key. This alters the
  OpenAPI output produced by `parameters_json_schema` (db engine specs) and by the app-wide Swagger
  spec / `superset update-api-docs`. It is **not code-breaking** but changes serialized output.
  Affected code:
  - `superset/db_engine_specs/gsheets.py` `catalog = fields.Dict()` ([L67](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67))
  - `superset/db_engine_specs/bigquery.py` `query = fields.Dict(required=False)` ([L213](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L213))
  - `superset/db_engine_specs/datastore.py` `query = fields.Dict(required=False)` ([L101](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L101))
  - plus every other `fields.Dict()` (no `values`) across `superset/**/schemas.py` that flows into
    the Swagger spec.

  This is the "known issue" the pre-existing pin comment referenced. Two test snapshots asserted the
  old output and were updated as part of this upgrade:
  - `tests/unit_tests/databases/api_test.py` (gsheets `catalog`) ([L286](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/unit_tests/databases/api_test.py#L286))
  - `tests/integration_tests/databases/api_tests.py` (bigquery `query`, gsheets `catalog`) ([L3519](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/databases/api_tests.py#L3519), [L3600](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/databases/api_tests.py#L3600))

### New functionality that can be used in the codebase

**None.** The only additions in 6.7.0 are official Python 3.13 support and dropping Python 3.8 —
neither is a usable apispec API feature for this codebase.

## Migration steps applied

1. Bumped the constraint `apispec>=6.0.0,<6.7.0` → `apispec>=6.0.0,<6.8.0` and removed the stale
   "known issue" comment in `requirements/base.in`.
2. Bumped the pin `apispec==6.6.1` → `apispec==6.7.0` in `requirements/base.txt` and
   `requirements/development.txt`.
3. Updated the two OpenAPI snapshot assertions above to include `"additionalProperties": {}` for the
   affected `fields.Dict()`-without-`values` fields.

The committed `docs/static/resources/openapi.json` is a manually-regenerated docs artifact (no CI
check regenerates or verifies it); it will pick up the `additionalProperties: {}` additions the next
time `superset update-api-docs` is run.
