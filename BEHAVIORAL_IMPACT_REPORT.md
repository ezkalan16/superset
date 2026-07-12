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

# `apispec` 6.7.0 Behavioral Impact Report

## Summary

The 6.7.0 fix for `fields.Dict()` with `values` unset adds `additionalProperties: {}` to the generated OpenAPI representation ([release source](https://github.com/marshmallow-code/apispec/blob/0b2ff4506f88ab2c011b4da0b8c2ccd508c536b1/CHANGELOG.rst#L7-L10)). A same-commit generation comparison between `apispec` 6.6.1 and 6.7.0 found 49 changed properties in Superset's main OpenAPI document and three changed database-parameter schemas.

The change makes the contract explicit that arbitrary property values are allowed. It does not change Marshmallow runtime loading, dumping, or validation, but generated API documentation, schema responses, snapshots, and downstream schema consumers can observe the added keyword.

## Impacted usages

| Generated schema property | Source usage | Likely effect |
| --- | --- | --- |
| `ChartDataAggregateOptionsSchema.aggregates` | [`ChartDataAggregateConfigField` and aggregate usage](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L464-L510) | Explicitly permits arbitrary aggregate mapping values. |
| `ChartDataSortOptionsSchema.aggregates` | [`ChartDataAggregateConfigField` sort usage](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L662-L675) | Explicitly permits arbitrary aggregate mapping values. |
| `ChartDataPivotOptionsSchema.aggregates` | [`ChartDataAggregateConfigField` pivot usage](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L860-L887) | Explicitly permits arbitrary aggregate mapping values. |
| `ChartDataSortOptionsSchema.columns` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L667-L674) | Explicitly permits arbitrary sort-column mapping values. |
| `ChartDataRollingOptionsSchema.rolling_type_options` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L578-L584) | Explicitly permits arbitrary rolling-operation options. |
| `ChartDataSelectOptionsSchema.rename[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L652-L659) | Each rename mapping item explicitly permits arbitrary properties. |
| `ChartDataPostProcessingOperation.options` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L977) | Explicitly permits operation-specific options. |
| `ChartDataQueryObject.applied_time_extras` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L1239) | Explicitly permits arbitrary temporal-extra entries. |
| `ChartEntityResponseSchema.form_data` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L219) | Explicitly permits arbitrary form-data keys. |
| `ChartDataResponseResult.data[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L1619) | Each returned data row explicitly permits arbitrary columns. |
| `ChartDataResponseResult.applied_filters[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L1628) | Each applied-filter object explicitly permits arbitrary properties. |
| `ChartDataResponseResult.rejected_filters[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L1631) | Each rejected-filter object explicitly permits arbitrary properties. |
| `DashboardPermalinkStateSchema.dataMask` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/permalink/schemas.py#L21) | Explicitly permits arbitrary data-mask entries. |
| `DashboardPermalinkStateSchema.chartStates` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/permalink/schemas.py#L61) | Explicitly permits arbitrary chart-state entries. |
| `DashboardDatasetSchema.column_formats` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L322) | Explicitly permits arbitrary column-format mappings. |
| `DashboardDatasetSchema.columns[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L346) | Each dataset column explicitly permits arbitrary properties. |
| `DashboardDatasetSchema.metrics[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L349) | Each dataset metric explicitly permits arbitrary properties. |
| `TableExtraMetadataResponseSchema.metadata` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L797) | Explicitly permits arbitrary table metadata. |
| `TableExtraMetadataResponseSchema.partitions` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L798) | Explicitly permits arbitrary partition metadata. |
| `TableExtraMetadataResponseSchema.clustering` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L799) | Explicitly permits arbitrary clustering metadata. |
| `DatabaseTablesResponse.extra` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L819) | Explicitly permits arbitrary extra metadata. |
| `ValidateSQLRequest.template_params` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L832) | Explicitly permits arbitrary template parameters. |
| `DatabaseRelatedDashboard.json_metadata` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L850) | Explicitly permits arbitrary dashboard metadata. |
| `DatasetRelatedDashboard.json_metadata` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/schemas.py#L228) | Explicitly permits arbitrary dashboard metadata. |
| `ExplorePermalinkStateSchema.formData` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/permalink/schemas.py#L21) | Explicitly permits arbitrary form-data keys. |
| `ExplorePermalinkStateSchema.chartState` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/permalink/schemas.py#L44) | Explicitly permits arbitrary chart-state keys. |
| `Dataset.column_formats` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L29) | Explicitly permits arbitrary column formats. |
| `Dataset.columns[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L30) | Each column entry explicitly permits arbitrary properties. |
| `Dataset.database` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L31) | Explicitly permits arbitrary database metadata. |
| `Dataset.extra` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L42) | Explicitly permits arbitrary dataset extras. |
| `Dataset.granularity_sqla[][]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L57) | Each nested granularity entry explicitly permits arbitrary properties. |
| `Dataset.metrics[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L73) | Each metric entry explicitly permits arbitrary properties. |
| `Dataset.params` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L84) | Explicitly permits arbitrary dataset parameters. |
| `Dataset.template_params` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L94) | Explicitly permits arbitrary template parameters. |
| `Dataset.verbose_map` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L103) | Explicitly permits arbitrary verbose-name mappings. |
| `Slice.form_data` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L134) | Explicitly permits arbitrary form-data properties. |
| `Slice.query_context` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L147) | Explicitly permits arbitrary query-context properties. |
| `ExploreContextSchema.form_data` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L156) | Explicitly permits arbitrary form-data keys. |
| `ReportScheduleRestApi.post.extra` | [`ReportSchedulePostSchema.extra`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/schemas.py#L261) | Explicitly permits arbitrary report-create extras. |
| `ReportScheduleRestApi.put.extra` | [`ReportSchedulePutSchema.extra`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/schemas.py#L425) | Explicitly permits arbitrary report-update extras. |
| `EstimateQueryCostSchema.template_params` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L44) | Explicitly permits arbitrary template parameters. |
| `QueryResult.extra` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L115) | Explicitly permits arbitrary result metadata. |
| `QueryExecutionResponseSchema.data[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L120) | Each result row explicitly permits arbitrary columns. |
| `QueryExecutionResponseSchema.columns[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L121) | Each column descriptor explicitly permits arbitrary properties. |
| `QueryExecutionResponseSchema.selected_columns[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L122) | Each selected-column descriptor explicitly permits arbitrary properties. |
| `QueryExecutionResponseSchema.expanded_columns[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L123) | Each expanded-column descriptor explicitly permits arbitrary properties. |
| `TabState.extra_json` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L142) | Explicitly permits arbitrary extra JSON. |
| `TabState.saved_query` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L148) | Explicitly permits arbitrary saved-query properties. |
| `RelatedResultResponse.extra` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/base_api.py#L70) | Explicitly permits arbitrary related-result metadata. |
| BigQuery `query` database parameter | [`BigQueryParametersSchema.query`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L208-L214) | The connection schema explicitly permits arbitrary query keys and values. |
| Datastore `query` database parameter | [`DatastoreParametersSchema.query`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L96-L102) | The connection schema explicitly permits arbitrary query keys and values. |
| Google Sheets `catalog` database parameter | [`GSheetsParametersSchema.catalog`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L66-L68) | The connection schema explicitly permits arbitrary catalog entries. |

## Human-review conclusion

The observable behavior change is limited to generated OpenAPI/JSON-schema output. `additionalProperties: {}` is semantically equivalent to the previous default that allowed arbitrary properties, so no request, response, or Marshmallow validation behavior changes. The resulting OpenAPI remains valid, but consumers that compare or snapshot exact schema text will observe the new keyword; Superset's three exact fixtures were updated accordingly.

The checked-in [`docs/static/resources/openapi.json`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/docs/static/resources/openapi.json) was reviewed but not regenerated in this upgrade. Running `superset update-api-docs` against this checkout also incorporates thousands of unrelated pre-existing documentation changes, so committing that generated diff would exceed the dependency-upgrade scope. The next intentional OpenAPI documentation refresh will include the 49 mechanical `additionalProperties: {}` additions described above and should receive human review with the other pending generated changes.
