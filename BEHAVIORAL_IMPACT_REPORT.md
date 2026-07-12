# Behavioral Impact Report: `apispec` 6.6.1 → 6.7.0 (for human review)

This report assesses the one "Changes to existing functionality" item from
`DEPENDENCY_UPGRADE_REPORT.md` for real behavioral impact on this codebase.

## Change under review

apispec 6.7.0 fixes the handling of `fields.Dict()` with `values` unset
([apispec #949](https://github.com/marshmallow-code/apispec/issues/949),
[CHANGELOG 6.7.0](https://github.com/marshmallow-code/apispec/blob/6.7.0/CHANGELOG.rst)).

- **Before (6.6.1):** a bare `fields.Dict()` rendered as `{"type": "object"}` — `additionalProperties` was omitted, which per OpenAPI means only an empty object validates.
- **After (6.7.0):** it renders as `{"type": "object", "additionalProperties": {}}` — i.e. an object with arbitrary properties (the intended meaning of `Dict()`).

## Does it affect THIS codebase's behavior?

**Yes — the generated OpenAPI documents change** (documentation output only; no
Python control flow, request handling, validation, or persisted data is affected).
The bare-`Dict` schema fields whose rendering changes are:

- [`superset/db_engine_specs/gsheets.py#L67`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67) — `catalog = fields.Dict()`
- [`superset/db_engine_specs/bigquery.py#L213`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L213) — `query = fields.Dict(required=False)`
- [`superset/db_engine_specs/datastore.py#L101`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L101) — `query = fields.Dict(required=False)`

These fields are surfaced through:

- **`GET /api/v1/_openapi`** and **`GET /api/v1/database/available`** — the JSON schemas for GSheets `catalog`, BigQuery `query`, and Datastore `query` now include `"additionalProperties": {}`.
- **`superset update-api-docs`** ([`superset/cli/update.py#L83`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L83)), which regenerates [`docs/static/resources/openapi.json`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/docs/static/resources/openapi.json). Re-running it after this upgrade will add `additionalProperties: {}` to those fields.
- **`parameters_json_schema()`** ([`superset/db_engine_specs/base.py#L2842`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2842)) for the affected engine specs, consumed by the database-connection UI.

## Likely effect

- **Low risk / net-positive.** The new output is more correct: it now advertises that these dictionaries accept arbitrary key/value pairs (which is how Superset actually uses them), instead of implying only an empty object is valid. The generated spec remains valid OpenAPI 3.0.2 (verified by `TestOpenApiSpec.test_open_api_spec`, [`tests/integration_tests/base_api_tests.py#L32`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/base_api_tests.py#L32)).
- **No runtime/validation behavior change.** Marshmallow load/validation of these fields is unchanged; only the *documented* JSON schema differs.
- **Action for maintainers:** the committed [`docs/static/resources/openapi.json`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/docs/static/resources/openapi.json) is a generated artifact. It was intentionally **not** wholesale-regenerated in this PR because regenerating it in an isolated environment produces a large, environment-dependent diff unrelated to this upgrade. When the docs are next regenerated via `superset update-api-docs`, expect `additionalProperties: {}` to appear on the three fields above. Any external consumers that validate payloads strictly against the old (stricter) schema for these fields would now accept a broader — and correct — set of inputs.
