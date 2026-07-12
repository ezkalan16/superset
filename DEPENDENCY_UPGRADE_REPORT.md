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

## Versions and research sources

- Current resolved version: `6.6.1` in [`requirements/base.txt`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.txt#L11) and [`requirements/development.txt`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/development.txt#L35).
- Previous source constraint: `apispec>=6.0.0,<6.7.0` in [`requirements/base.in`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/requirements/base.in#L43-L45).
- Target version: `6.7.0`.
- DeepWiki was queried first. `marshmallow-code/apispec` was indexed and identified `CHANGELOG.rst` and the `MarshmallowPlugin` field-conversion path; `ezkalan16/superset` was not indexed, so all Superset findings below were derived from and verified against commit `6a8619bd4f643f634b3beb3cce1f902cd4ff80a1`.
- Official sources reviewed: [`apispec` 6.7.0 changelog](https://github.com/marshmallow-code/apispec/blob/0b2ff4506f88ab2c011b4da0b8c2ccd508c536b1/CHANGELOG.rst#L4-L15), [`fields.Dict()` issue #949](https://github.com/marshmallow-code/apispec/issues/949), and the [official upgrading guide](https://apispec.readthedocs.io/en/6.7.0/upgrading.html), which contains no 6.7-specific migration instructions.

## Breaking changes

None.

`apispec` 6.7.0 removes or renames no public API used by Superset and changes no relevant call signature. The dropped Python 3.8 support is not breaking for this repository because [`pyproject.toml`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/pyproject.toml#L27) requires Python `>=3.10`.

## New deprecations

None.

No API used by this codebase is newly deprecated between 6.6.1 and 6.7.0.

## Changes to existing functionality

- `MarshmallowPlugin` now emits `additionalProperties: {}` for `fields.Dict()` fields whose `values` argument is unset ([6.7.0 changelog](https://github.com/marshmallow-code/apispec/blob/0b2ff4506f88ab2c011b4da0b8c2ccd508c536b1/CHANGELOG.rst#L7-L10)). This changes generated OpenAPI schemas for untyped dictionaries used by [chart schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L219), [dashboard schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L322), [database schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L797-L850), [dataset schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/schemas.py#L228), [Explore schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L29-L156), [report schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/schemas.py#L261-L425), [SQL Lab schemas](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L44-L148), the [related-result schema](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/base_api.py#L70), and the [BigQuery](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L208-L214), [Datastore](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L96-L102), and [Google Sheets](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L66-L68) database parameter schemas. The exact generated-property inventory and behavioral assessment are in `BEHAVIORAL_IMPACT_REPORT.md`.

## New functionality that can be used in the codebase

None.

The only other release changes are official Python 3.13 support and dropping Python 3.8; neither provides a new `apispec` API or simplification applicable to Superset.

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

Flask-AppBuilder's `add_api_spec()` consumes Superset's `openapi_spec_tag`, `openapi_spec_component_schemas`, `apispec_parameter_schemas`, and `openapi_spec_methods` configuration. Every current integration site is grouped below.

| Area | Configuration usage |
| --- | --- |
| Advanced data types | [`superset/advanced_data_type/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/advanced_data_type/api.py#L51-L55) |
| Annotation layers | [`superset/annotation_layers/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/annotation_layers/api.py#L110-L114) and [`annotations/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/annotation_layers/annotations/api.py#L118-L122) |
| Available domains and cache invalidation | [`available_domains/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/available_domains/api.py#L37-L38) and [`cachekeys/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/cachekeys/api.py#L45) |
| Charts and CSS templates | [`charts/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/api.py#L267-L278) and [`css_templates/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/css_templates/api.py#L93-L97) |
| Dashboards | [`dashboards/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/api.py#L479-L498), [`filter_state/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/filter_state/api.py#L37), and [`permalink/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/permalink/api.py#L45-L46) |
| Databases and datasets | [`databases/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/api.py#L285-L313), [`datasets/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/api.py#L293-L352), [`columns/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/columns/api.py#L46), and [`metrics/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/metrics/api.py#L46) |
| Datasources and embedded dashboards | [`datasource/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasource/api.py#L52) and [`embedded/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/embedded/api.py#L56-L57) |
| Explore and import/export | [`explore/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/api.py#L45-L46), [`form_data/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/form_data/api.py#L47-L48), [`permalink/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/permalink/api.py#L49-L50), and [`importexport/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/importexport/api.py#L43) |
| Queries | [`queries/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/queries/api.py#L73-L76), [additional query configuration](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/queries/api.py#L138-L140), and [`saved_queries/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/queries/saved_queries/api.py#L177-L182) |
| Reports | [`reports/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/api.py#L278-L282) and [`reports/logs/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/logs/api.py#L87-L88) |
| RLS, security, and semantic layers | [`row_level_security/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/row_level_security/api.py#L78-L167), [`security/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/security/api.py#L156-L269), and [`semantic_layers/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/semantic_layers/api.py#L542) |
| SQL Lab | [`sqllab/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/api.py#L89-L97) and [`sqllab/permalink/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/permalink/api.py#L41-L42) |
| Tags, tasks, and themes | [`tags/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/tags/api.py#L142-L153), [`tasks/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/tasks/api.py#L149-L156), and [`themes/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/themes/api.py#L141-L146) |
| Base, logs, and users | [`views/base_api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/base_api.py#L376-L382), [`views/log/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/log/api.py#L77-L85), and [`views/users/api.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/users/api.py#L43-L45) |

### Generated output and validation consumers

- [`docs/static/resources/openapi.json`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/docs/static/resources/openapi.json) is written by `update_api_docs`.
- [`tests/integration_tests/base_api_tests.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/base_api_tests.py#L31-L43) validates the live OpenAPI document.
- Exact database-parameter schema fixtures are asserted in [`tests/unit_tests/databases/api_test.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/unit_tests/databases/api_test.py#L283-L289) and [`tests/integration_tests/databases/api_tests.py`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/tests/integration_tests/databases/api_tests.py#L3516-L3522).

## Migration steps

1. Replaced the former range and known-issue ceiling with the exact requested source pin `apispec==6.7.0`.
2. Regenerated the runtime and development locks so both resolve `apispec==6.7.0`.
3. Updated the BigQuery and Google Sheets schema fixtures to expect the intentional `additionalProperties: {}` output.
4. No application API migration was required because 6.7.0 removes no API used by Superset and introduces no applicable deprecation.
5. Documented the observable generated-schema change in `BEHAVIORAL_IMPACT_REPORT.md`.
