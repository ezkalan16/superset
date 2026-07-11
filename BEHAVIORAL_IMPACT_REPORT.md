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

The change makes the contract explicit that arbitrary property values are allowed. It does not change Marshmallow runtime loading, dumping, or validation, and it does not require application-code changes. Human review is requested because generated API documentation and schema consumers can observe the added keyword.

## Impacted usages

| Generated schema property | Source usage | Likely effect |
| --- | --- | --- |
| `ChartDataAggregateOptionsSchema.aggregates` | [`ChartDataAggregateConfigField` and aggregate usage](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L464-L510) | Generated schema explicitly permits arbitrary aggregate mapping values. |
| `ChartDataSortOptionsSchema.aggregates` | [`ChartDataAggregateConfigField` sort usage](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L662-L675) | Generated schema explicitly permits arbitrary aggregate mapping values. |
| `ChartDataPivotOptionsSchema.aggregates` | [`ChartDataAggregateConfigField` pivot usage](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L860-L887) | Generated schema explicitly permits arbitrary aggregate mapping values. |
| `ChartDataSortOptionsSchema.columns` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L667-L674) | Generated schema explicitly permits arbitrary sort-column mapping values. |
| `ChartDataRollingOptionsSchema.rolling_type_options` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L578-L584) | Generated schema explicitly permits arbitrary rolling-operation options. |
| `ChartDataSelectOptionsSchema.rename[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L652-L659) | Each rename mapping item explicitly permits arbitrary properties. |
| `ChartDataPostProcessingOperation.options` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L977) | Generated schema explicitly permits operation-specific options. |
| `ChartDataQueryObject.applied_time_extras` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L1239) | Generated schema explicitly permits arbitrary temporal-extra entries. |
| `ChartEntityResponseSchema.form_data` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L219) | Generated chart response schema explicitly permits arbitrary form-data keys. |
| `ChartDataResponseResult.data[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L1619) | Each returned data row explicitly permits arbitrary columns. |
| `ChartDataResponseResult.applied_filters[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L1628) | Each applied-filter object explicitly permits arbitrary properties. |
| `ChartDataResponseResult.rejected_filters[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/charts/schemas.py#L1631) | Each rejected-filter object explicitly permits arbitrary properties. |
| `DashboardPermalinkStateSchema.dataMask` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/permalink/schemas.py#L21) | Generated permalink state explicitly permits arbitrary data-mask entries. |
| `DashboardPermalinkStateSchema.chartStates` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/permalink/schemas.py#L61) | Generated permalink state explicitly permits arbitrary chart-state entries. |
| `DashboardDatasetSchema.column_formats` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L322) | Generated schema explicitly permits arbitrary column-format mappings. |
| `DashboardDatasetSchema.columns[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L346) | Each dashboard dataset column object explicitly permits arbitrary properties. |
| `DashboardDatasetSchema.metrics[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/dashboards/schemas.py#L349) | Each dashboard dataset metric object explicitly permits arbitrary properties. |
| `TableExtraMetadataResponseSchema.metadata` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L797) | Generated table metadata explicitly permits arbitrary properties. |
| `TableExtraMetadataResponseSchema.partitions` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L798) | Generated partition metadata explicitly permits arbitrary properties. |
| `TableExtraMetadataResponseSchema.clustering` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L799) | Generated clustering metadata explicitly permits arbitrary properties. |
| `DatabaseTablesResponse.extra` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L819) | Generated database-table response explicitly permits arbitrary extra metadata. |
| `ValidateSQLRequest.template_params` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L832) | Generated request schema explicitly permits arbitrary template parameters. |
| `DatabaseRelatedDashboard.json_metadata` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/databases/schemas.py#L850) | Generated related-dashboard metadata explicitly permits arbitrary properties. |
| `DatasetRelatedDashboard.json_metadata` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/datasets/schemas.py#L228) | Generated related-dashboard metadata explicitly permits arbitrary properties. |
| `ExplorePermalinkStateSchema.formData` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/permalink/schemas.py#L21) | Generated permalink form data explicitly permits arbitrary keys. |
| `ExplorePermalinkStateSchema.chartState` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/permalink/schemas.py#L44) | Generated permalink chart state explicitly permits arbitrary keys. |
| `Dataset.column_formats` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L29) | Generated Explore dataset schema explicitly permits arbitrary column formats. |
| `Dataset.columns[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L30) | Each generated column entry explicitly permits arbitrary properties. |
| `Dataset.database` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L31) | Generated database metadata explicitly permits arbitrary properties. |
| `Dataset.extra` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L42) | Generated dataset extras explicitly permit arbitrary properties. |
| `Dataset.granularity_sqla[][]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L57) | Each nested granularity entry explicitly permits arbitrary properties. |
| `Dataset.metrics[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L73) | Each generated metric entry explicitly permits arbitrary properties. |
| `Dataset.params` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L84) | Generated dataset parameters explicitly permit arbitrary properties. |
| `Dataset.template_params` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L94) | Generated template parameters explicitly permit arbitrary properties. |
| `Dataset.verbose_map` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L103) | Generated verbose-name mapping explicitly permits arbitrary values. |
| `Slice.form_data` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L134) | Generated slice form data explicitly permits arbitrary properties. |
| `Slice.query_context` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L147) | Generated slice query context explicitly permits arbitrary properties. |
| `ExploreContextSchema.form_data` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/explore/schemas.py#L156) | Generated Explore context explicitly permits arbitrary form-data keys. |
| `ReportScheduleRestApi.post.extra` | [`ReportSchedulePostSchema.extra`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/schemas.py#L261) | Generated report-create extras explicitly permit arbitrary properties. |
| `ReportScheduleRestApi.put.extra` | [`ReportSchedulePutSchema.extra`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/reports/schemas.py#L425) | Generated report-update extras explicitly permit arbitrary properties. |
| `EstimateQueryCostSchema.template_params` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L44) | Generated cost-estimation request explicitly permits arbitrary template parameters. |
| `QueryResult.extra` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L115) | Generated query result explicitly permits arbitrary extra metadata. |
| `QueryExecutionResponseSchema.data[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L120) | Each result data row explicitly permits arbitrary columns. |
| `QueryExecutionResponseSchema.columns[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L121) | Each column descriptor explicitly permits arbitrary properties. |
| `QueryExecutionResponseSchema.selected_columns[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L122) | Each selected-column descriptor explicitly permits arbitrary properties. |
| `QueryExecutionResponseSchema.expanded_columns[]` | [Nested `fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L123) | Each expanded-column descriptor explicitly permits arbitrary properties. |
| `TabState.extra_json` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L142) | Generated tab state explicitly permits arbitrary extra JSON. |
| `TabState.saved_query` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/sqllab/schemas.py#L148) | Generated tab state explicitly permits arbitrary saved-query properties. |
| `RelatedResultResponse.extra` | [`fields.Dict()`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/views/base_api.py#L70) | Generated related-result metadata explicitly permits arbitrary properties. |
| BigQuery `query` database parameter | [`BigQueryParametersSchema.query`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/bigquery.py#L208-L214) | Database-connection parameter JSON schema now explicitly permits arbitrary query keys and values. |
| Datastore `query` database parameter | [`DatastoreParametersSchema.query`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/datastore.py#L96-L102) | Database-connection parameter JSON schema now explicitly permits arbitrary query keys and values. |
| Google Sheets `catalog` database parameter | [`GSheetsParametersSchema.catalog`](https://github.com/ezkalan16/superset/blob/6a8619bd4f643f634b3beb3cce1f902cd4ff80a1/superset/db_engine_specs/gsheets.py#L66-L68) | Database-connection parameter JSON schema now explicitly permits arbitrary catalog entries. |
