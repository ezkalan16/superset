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

# `apispec` 6.7.0 Dependency Upgrade Report

## Versions

- Current resolved version: `6.6.1` in [`requirements/base.txt`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.txt#L11) and [`requirements/development.txt`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/development.txt#L35).
- Previous source constraint: `apispec>=6.0.0,<6.7.0` in [`requirements/base.in`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.in#L43-L45).
- Target version: `6.7.0`.
- Release source: [`apispec` 6.7.0 changelog](https://github.com/marshmallow-code/apispec/blob/0b2ff4506f88ab2c011b4da0b8c2ccd508c536b1/CHANGELOG.rst#L4-L15).

## Breaking changes

None.

## New deprecations

None.

## Changes to existing functionality

- `MarshmallowPlugin` now emits `additionalProperties: {}` for `fields.Dict()` fields whose `values` argument is unset ([6.7.0 changelog](https://github.com/marshmallow-code/apispec/blob/0b2ff4506f88ab2c011b4da0b8c2ccd508c536b1/CHANGELOG.rst#L7-L10)); this changes generated OpenAPI schemas for untyped dictionaries used by the [chart schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L219), [dashboard schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L322), [database schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L797-L850), [dataset schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/schemas.py#L228), [Explore schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L29-L156), [report schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/schemas.py#L261-L425), [SQL Lab schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L44-L148), [related-result schema](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/base_api.py#L70), and the [BigQuery](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L208-L214), [Datastore](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L96-L102), and [Google Sheets](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L66-L68) database parameter schemas. The exact generated-property inventory and behavioral assessment are in `BEHAVIORAL_IMPACT_REPORT.md`.

## New functionality that can be used in the codebase

None.

## Other release changes assessed as not applicable

- Official Python 3.13 support does not require a migration; Superset already declares Python `>=3.10`.
- Dropping Python 3.8 support does not affect Superset because the repository requires Python `>=3.10`.

## Usage inventory

### Dependency and tooling references

| File | Usage |
| --- | --- |
| [`requirements/base.in`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.in#L43-L45) | Declares the source dependency constraint. |
| [`requirements/base.txt`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.txt#L11-L14) | Pins the resolved runtime version. |
| [`requirements/development.txt`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/development.txt#L35-L38) | Pins the resolved development version. |
| [`pyproject.toml`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/pyproject.toml#L259) | Classifies `apispec` as a known third-party import for import sorting. |

### Direct imports and API calls

| Area | Usage |
| --- | --- |
| OpenAPI document generator | Imports `APISpec` and `MarshmallowPlugin`, constructs the document, delegates each Flask-AppBuilder API through `add_api_spec`, and serializes `to_dict()` in [`superset/cli/update.py:24-25,83-98`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cli/update.py#L24-L98). |
| Temporary cache API | Imports `APISpec` and `DuplicateComponentNameError`, registers two schemas through `components.schema()`, and delegates to the parent implementation in [`superset/temporary_cache/api.py:22-23,57-67`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/temporary_cache/api.py#L22-L67). |
| Base database engine | [Imports `APISpec` and `MarshmallowPlugin`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L43-L44), then [constructs a spec, registers `parameters_schema`, and extracts it from `to_dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/base.py#L2850-L2857). |
| BigQuery engine | [Imports both classes](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L29-L30), [instantiates a module plugin](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L200), then [constructs a spec, registers `parameters_schema`, and calls `to_dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L981-L991). |
| Databricks engine | [Imports both classes](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L23-L24), then [constructs a spec, registers `properties_schema`, and calls `to_dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/databricks.py#L708-L715). |
| Datastore engine | [Imports both classes](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L27-L28), [instantiates a module plugin](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L93), then [constructs a spec, registers `parameters_schema`, and calls `to_dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L459-L469). |
| DuckDB engine | [Imports both classes](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L25-L26), then [constructs a spec, registers `parameters_schema`, and calls `to_dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/duckdb.py#L183-L190). |
| Google Sheets engine | [Imports both classes and instantiates a module plugin](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L26-L63), then [constructs a spec, registers `parameters_schema`, and calls `to_dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L342-L352). |
| Snowflake engine | [Imports both classes](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L26-L27), then [constructs a plugin and spec, registers `parameters_schema`, and calls `to_dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/snowflake.py#L425-L434). |

### Indirect Flask-AppBuilder integration

The following API class attributes and overrides are consumed by Flask-AppBuilder's `add_api_spec()` implementation and therefore indirectly configure `apispec`:

| Area | Configuration usage |
| --- | --- |
| Advanced data types | [`openapi_spec_tag`, `apispec_parameter_schemas`, component schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/advanced_data_type/api.py#L51-L55) |
| Annotation layers | [Layer API configuration](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/annotation_layers/api.py#L110-L114) and [annotation API configuration](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/annotation_layers/annotations/api.py#L118-L122) |
| Available domains | [Tag and component schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/available_domains/api.py#L37-L38) |
| Cache invalidation | [Component schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cachekeys/api.py#L45) |
| Charts | [Tag, component schemas, parameter schemas, and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/api.py#L267-L278) |
| CSS templates | [Parameter schemas, tag, and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/css_templates/api.py#L93-L97) |
| Dashboards | [Tag, component schemas, parameter schemas, and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/api.py#L479-L498), [filter-state tag](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/filter_state/api.py#L37), and [permalink tag/components](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/permalink/api.py#L45-L46) |
| Databases | [Parameter schemas, tag, component schemas, and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/api.py#L285-L313) |
| Datasets | [Tag, parameter schemas, component schemas, and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/api.py#L293-L352), plus [column](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/columns/api.py#L46) and [metric](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/metrics/api.py#L46) tags |
| Datasources | [Tag](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasource/api.py#L52) |
| Embedded dashboards | [Tag and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/embedded/api.py#L56-L57) |
| Explore | [Tag and component schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/api.py#L45-L46), [form-data tag/components](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/form_data/api.py#L47-L48), and [permalink tag/components](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/permalink/api.py#L49-L50) |
| Import/export | [Tag](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/importexport/api.py#L43) |
| Queries | [Parameter schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/queries/api.py#L73-L76), [tag, method overrides, and component schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/queries/api.py#L138-L140), and [saved-query configuration](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/queries/saved_queries/api.py#L177-L182) |
| Reports | [Parameter schemas, tag, and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/api.py#L278-L282) and [report-log configuration](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/logs/api.py#L87-L88) |
| Row-level security | [Tag and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/row_level_security/api.py#L78-L167) |
| Security | [Security tags and role component schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/security/api.py#L156-L269) |
| Semantic layers | [Tag](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/semantic_layers/api.py#L542) |
| SQL Lab | [Parameter schemas, tag, and component schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/api.py#L89-L97) and [permalink tag/components](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/permalink/api.py#L41-L42) |
| Tags | [Tag, component schemas, parameter schemas, and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/tags/api.py#L142-L153) |
| Tasks | [Tag, component schemas, and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/tasks/api.py#L149-L156) |
| Themes | [Parameter schemas, tag, and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/themes/api.py#L141-L146) |
| Base API | [Dynamically extends parameter and component schema configuration](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/base_api.py#L376-L382) |
| Logs | [Parameter schemas, component schemas, and method overrides](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/log/api.py#L77-L85) |
| Users | [Current-user tag/components](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/users/api.py#L43-L45) and [user tag/components](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/users/api.py#L169-L173) |

The `openapi_spec_methods` values above are defined in:

- [`superset/annotation_layers/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/annotation_layers/schemas.py#L20), [`superset/annotation_layers/annotations/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/annotation_layers/annotations/schemas.py#L24), [`superset/charts/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L186), and [`superset/css_templates/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/css_templates/schemas.py#L18).
- [`superset/dashboards/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L81), [`superset/databases/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L184), [`superset/datasets/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/schemas.py#L48), and [`superset/queries/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/queries/schemas.py#L24).
- [`superset/queries/saved_queries/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/queries/saved_queries/schemas.py#L28), [`superset/reports/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/schemas.py#L35), [`superset/reports/logs/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/logs/schemas.py#L18), and [`superset/row_level_security/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/row_level_security/schemas.py#L63).
- [`superset/tags/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/tags/schemas.py#L26), [`superset/tasks/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/tasks/schemas.py#L193), [`superset/themes/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/themes/schemas.py#L170), and [`superset/views/log/schemas.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/log/schemas.py#L29).

### Generated output and validation consumers

- [`docs/static/resources/openapi.json`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/docs/static/resources/openapi.json) is the generated document written by `update_api_docs`.
- [`tests/integration_tests/base_api_tests.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/base_api_tests.py#L31-L43) validates the live OpenAPI document with `openapi-spec-validator`.
- [`tests/integration_tests/db_engine_specs/postgres_tests.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/db_engine_specs/postgres_tests.py#L479-L503) checks exact generated database-parameter schema content.

## Migration steps

1. Replace the former range and known-issue ceiling with the exact requested source pin `apispec==6.7.0`.
2. Regenerate `requirements/base.txt` and `requirements/development.txt` with `./scripts/uv-pip-compile.sh`.
3. No source API migration is required because 6.7.0 removes no API used by Superset and introduces no applicable deprecation.
4. Review the intentional OpenAPI output change documented in `BEHAVIORAL_IMPACT_REPORT.md`; runtime Marshmallow loading and dumping behavior is unchanged.
