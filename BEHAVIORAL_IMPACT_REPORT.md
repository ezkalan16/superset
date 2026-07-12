# Behavioral Impact Report — `apispec` 6.6.1 → 6.7.0 (for human review)

This report covers the **"Changes to existing functionality"** category from
`DEPENDENCY_UPGRADE_REPORT.md`, assessed for actual behavioral impact on this codebase given how it
uses the affected functionality.

- **Dependency:** `apispec` `6.6.1` → `6.7.0`
- **Analyzed commit:** `6a8619bd4f643f634b3beb3cce1f902cd4ff80a1`

## Change assessed

**apispec [#949](https://github.com/marshmallow-code/apispec/issues/949):** in `dict2properties`,
a `marshmallow.fields.Dict()` whose `values`/`value_field` is unset now emits
`"additionalProperties": {}` in the generated OpenAPI property. In 6.6.1 the same field produced
`{"type": "object"}` with no `additionalProperties` key. Fields that set `values=...` (e.g.
`fields.Dict(keys=fields.Str(), values=fields.Raw())`) are unchanged.

Empirically verified in a clean venv:

```
# apispec 6.6.1
{"a": {"type": "object"}, "b": {"type": "object", "additionalProperties": {}}}
# apispec 6.7.0
{"a": {"type": "object", "additionalProperties": {}}, "b": {"type": "object", "additionalProperties": {}}}
#   where a = fields.Dict(), b = fields.Dict(keys=fields.Str(), values=fields.Raw())
```

## Does it impact THIS codebase?

**Yes — the generated OpenAPI/Swagger output changes**, but there is **no change to runtime request
handling, validation, or data flow.** The affected output is the JSON schema Superset generates from
marshmallow schemas via apispec:

1. **`db_engine_specs` `parameters_json_schema()`** — returned to the frontend by
   `/api/v1/database/available` and `/api/v1/database/<id>/connection` and used to render the DB
   connection form. Affected fields (bare `fields.Dict()` without `values`):
   - `superset/db_engine_specs/gsheets.py` `catalog = fields.Dict()` —
     [L67](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67)
     → `catalog` now serializes as `{"type": "object", "additionalProperties": {}}`.
   - `superset/db_engine_specs/bigquery.py` `query = fields.Dict(required=False)` —
     [L213](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L213)
     → `query` now serializes as `{"type": "object", "additionalProperties": {}}`.
   - `superset/db_engine_specs/datastore.py` `query = fields.Dict(required=False)` —
     [L101](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L101).

2. **The app-wide Swagger spec** (`/swagger/v1`, and the committed
   `docs/static/resources/openapi.json` produced by `superset update-api-docs` via
   [`superset/cli/update.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L83))
   — every marshmallow schema containing a bare `fields.Dict()` (no `values`) in
   `superset/**/schemas.py` gains `"additionalProperties": {}` on those properties.

### Likely effect

- **Semantics unchanged.** In JSON Schema / OpenAPI, an `object` with no `additionalProperties` and
  the same `object` with `additionalProperties: {}` (empty-schema = "allow any") both permit
  arbitrary additional properties. So request validation and API behavior are equivalent.
- **Observable output diff.** API consumers that snapshot or byte-compare the OpenAPI/Swagger output
  (or the DB connection parameter schema) will see the added `additionalProperties: {}` keys. This
  is why two in-repo snapshot tests required updating (done in the upgrade PR):
  `tests/unit_tests/databases/api_test.py` and `tests/integration_tests/databases/api_tests.py`.
- **Docs artifact.** `docs/static/resources/openapi.json` is not regenerated/verified by CI; it will
  reflect the new output the next time `superset update-api-docs` runs. No code action required.

## Recommendation for reviewers

No functional/runtime behavior change to act on. Confirm you are comfortable with the additive
`additionalProperties: {}` keys in the generated OpenAPI/Swagger output, and (optionally) regenerate
`docs/static/resources/openapi.json` via `superset update-api-docs` in a follow-up so the committed
docs artifact matches the new serialization.
