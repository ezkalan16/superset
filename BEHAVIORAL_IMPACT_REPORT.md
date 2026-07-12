# Behavioral Impact Report — `apispec` 6.6.1 → 6.7.0

**For human review.**

- **Dependency:** `apispec`
- **Current version:** `6.6.1`
- **Target version:** `6.7.0`
- **Repository:** https://github.com/ezkalan16/superset
- **Base commit for links:** `6a8619bd4f643f634b3beb3cce1f902cd4ff80a1`

This report assesses the one item in the "Changes to existing functionality"
category of `DEPENDENCY_UPGRADE_REPORT.md` for whether it actually affects the
behavior of this codebase.

## Behavioral change

**`fields.Dict()` with `values` unset now renders `additionalProperties: {}`.**

In `6.6.1`, a `marshmallow.fields.Dict` declared without a `values` argument was
rendered into OpenAPI as `{"type": "object"}` (with `additionalProperties`
omitted). In `6.7.0` (issue
[#949](https://github.com/marshmallow-code/apispec/issues/949), PR
[#950](https://github.com/marshmallow-code/apispec/pull/950)) it is rendered as
`{"type": "object", "additionalProperties": {}}`, explicitly signalling that
arbitrary values are allowed. Verified locally:

```
# fields.Dict()               6.6.1 -> {"type": "object"}
#                             6.7.0 -> {"type": "object", "additionalProperties": {}}
# fields.Dict(required=False) 6.6.1 -> {"type": "object"}
#                             6.7.0 -> {"type": "object", "additionalProperties": {}}
# fields.Dict(values=Raw())   6.6.1 -> {"type": "object", "additionalProperties": {}}  (unchanged)
```

## Does it affect this codebase's behavior?

**Yes — but only in the generated OpenAPI specification / Swagger UI, not in
runtime request/response handling.**

Superset validates and deserializes request bodies with marshmallow (e.g.
`schema.load(...)`), not with the emitted OpenAPI document. The OpenAPI schema
produced via `APISpec` + `MarshmallowPlugin` is consumed by:

- the Swagger UI / `/openapi` document served to API clients, and
- the db-engine-spec `parameters_json_schema()` output that the frontend uses to
  render database-connection forms.

For every `fields.Dict()` without `values`, that document now contains
`additionalProperties: {}`. Semantically this is the correct/looser description
(the previous form implied an object with no permitted properties under strict
readers), so the change should be neutral-to-positive for downstream consumers.
No request that previously succeeded will now fail, because request validation is
unchanged.

### Impacted usage sites

Directly exercised by tests (db-engine-spec connection-parameter schemas):

- `bigquery` `query` — [superset/db_engine_specs/bigquery.py#L213](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L213)
- `gsheets` `catalog` — [superset/db_engine_specs/gsheets.py#L67](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67)
- `datastore` `query` — [superset/db_engine_specs/datastore.py#L101](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L101)

Representative REST-API schema fields whose rendered OpenAPI now gains
`additionalProperties: {}` (documentation-only effect):

- [superset/dashboards/schemas.py#L190](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L190) (`chart_configuration`, `filter_scopes`, `expanded_slices`, ...)
- [superset/charts/schemas.py#L1755](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L1755) (`params`) and [#L219](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L219) (`form_data`)
- [superset/databases/schemas.py#L797-L799](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L797) (`metadata`, `partitions`, `clustering`)
- [superset/datasets/schemas.py#L228](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/schemas.py#L228) (`json_metadata`, `extra`, `params`, `template_params`)
- [superset/explore/schemas.py#L29](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L29) (`column_formats`, `params`, `template_params`, ...)
- [superset/sqllab/schemas.py#L142](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L142) (`extra_json`, `template_params`, ...)

## Likely effect / recommended human check

- **Effect:** The published OpenAPI/Swagger documentation and the
  `parameters_json_schema` payloads consumed by the database-connection UI will
  now explicitly allow arbitrary key/value pairs on these object fields. This
  matches the intended meaning of an untyped `Dict`.
- **Risk:** Low. Runtime API validation is unchanged. The only observable
  differences are (a) the OpenAPI document content and (b) any external client
  that snapshots/validates against Superset's OpenAPI spec, which will see the
  added `additionalProperties: {}`.
- **Recommended check:** If any downstream tooling pins or diffs Superset's
  OpenAPI document, regenerate/update those snapshots. No application code change
  is required.
