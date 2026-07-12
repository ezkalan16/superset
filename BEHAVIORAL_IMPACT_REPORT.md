# Behavioral Impact Report — `apispec` 6.6.1 → 6.7.0 (for human review)

This report covers the single "Changes to existing functionality" item from
`DEPENDENCY_UPGRADE_REPORT.md` and whether it actually changes the behavior of
this codebase.

- **Base commit for links:** `6a8619bd4f643f634b3beb3cce1f902cd4ff80a1`

## Behavioral change

apispec 6.7.0 fixes the handling of `fields.Dict()` when `values` is **not**
set ([issue #949](https://github.com/marshmallow-code/apispec/issues/949)).
Verified empirically against both versions with a bare `fields.Dict()`:

| apispec | Generated schema for a bare `fields.Dict()` |
| --- | --- |
| 6.6.1 | `{"type": "object"}` |
| 6.7.0 | `{"type": "object", "additionalProperties": {}}` |

`fields.Dict(..., values=fields.Raw())` already produced `additionalProperties: {}`
on both versions, so only **bare** `fields.Dict()` declarations change.

This is a **spec-generation output change**. apispec is only used in Superset to
*emit* OpenAPI/JSON-schema documents; it does not validate incoming requests
(marshmallow does that, and marshmallow's `fields.Dict()` runtime behavior is
unchanged). So the change affects the *content of generated schema documents*,
not request parsing, data loading, or any runtime code path.

## Impacted usage sites and likely effect

### 1. Database connection parameter schemas

`BaseEngineSpec.parameters_json_schema()`
([`superset/db_engine_specs/base.py#L2850`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2850))
builds an `APISpec` and returns the resulting JSON schema. It is exposed to the
frontend "Connect a database" flow via `/api/v1/database/available`. The bare
`fields.Dict()` fields affected are:

- [`superset/db_engine_specs/gsheets.py#L67`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L67) — `catalog`
- [`superset/db_engine_specs/bigquery.py#L213`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L213) — `query`
- [`superset/db_engine_specs/datastore.py#L101`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L101) — `query`

**Effect:** the `catalog`/`query` properties in the emitted schema gain
`"additionalProperties": {}`. `additionalProperties: {}` (an empty schema) is
semantically equivalent to the OpenAPI default of "any additional properties
are allowed" — i.e. no new constraint is imposed and no previously-valid value
becomes invalid. The frontend consumes these fields as free-form key/value
inputs and does not branch on the presence of `additionalProperties`
(see [`superset-frontend/src/features/databases/types.ts#L163`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset-frontend/src/features/databases/types.ts#L163)),
so the rendered connection form is unchanged. The pre-existing frontend fixture
for the base (`values=fields.Raw()`) `query` field already contains
`additionalProperties: {}`
([`DatabaseModal/index.test.tsx#L141`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset-frontend/src/features/databases/DatabaseModal/index.test.tsx#L141)),
confirming the shape is already expected by the UI.

### 2. Main OpenAPI document (`/api/v1/_openapi` and `superset update-api-docs`)

Flask-AppBuilder renders every REST API schema into the OpenAPI document. Bare
`fields.Dict()` fields there include
[`views/base_api.py#L70`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/base_api.py#L70)
(`RelatedResponseSchema.extra`), and fields in
[`sqllab/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L115),
[`reports/schemas.py#L425`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/schemas.py#L425),
and [`semantic_layers/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/semantic_layers/schemas.py#L36).

**Effect:** those object properties gain `"additionalProperties": {}` in the
published OpenAPI doc. The document remains a valid OpenAPI 3.0 spec —
`tests/integration_tests/base_api_tests.py::TestOpenApiSpec::test_open_api_spec`
([L32](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/base_api_tests.py#L32))
runs `openapi_spec_validator.validate()` against the live document and still
passes. No runtime endpoint behavior changes; only the self-describing schema
text changes.

## Conclusion

The behavioral change is limited to the **text of generated OpenAPI/JSON schema
documents**: a semantically-neutral `additionalProperties: {}` is added to
object properties declared with a bare `fields.Dict()`. There is **no impact on
request validation, data processing, connection handling, or any runtime code
path**, and the resulting documents remain valid and semantically equivalent.
The only concrete change required was updating hard-coded expected schema values
in three test fixtures (see `DEPENDENCY_UPGRADE_REPORT.md`). No further human
action is required, but reviewers who pin or snapshot the generated
`openapi.json` / `/api/v1/database/available` responses downstream should expect
the added `additionalProperties: {}` keys.
