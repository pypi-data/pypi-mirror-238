# Changelog

## 0.7.6 - 2023-10-26

* Fetch Domo audits up to yesterday date

## 0.7.5 - 2023-10-26

* Add `escapechar` in csv serialisation

## 0.7.4 - 2023-10-23

* Pick the most recent sharded tables in `BigQuery`

## 0.7.3 - 2023-10-19

* Add retry mechanism to LookerClient when multithreading

## 0.7.2 - 2023-10-19

* pycryptodome moved as an optional dependency for extras: metabase and all

## 0.7.1 - 2023-10-04

* Fix thread pool size verification

## 0.7.0 - 2023-10-02

* Add option to fetch Looker Looks & Dashboards per folder

## 0.6.3 - 2023-10-02

* Add refreshing mechanism for Domo authentication tokens

## 0.6.2 - 2023-09-29

* Update field_size_limit in CSVFormatter

## 0.6.1 - 2023-09-25

* Add support for Domo

## 0.6.0 - 2023-09-25

* Move msal dependencies to powerbi extra

## 0.5.10 - 2023-09-25

* Retrieve column_id instead of object_id for Snowflake column tags

## 0.5.9 - 2023-09-21

* Add column tags for Snowflake

## 0.5.8 - 2023-09-19

* Remove non-used dependencies
* Fix some import in tests
* Clean pyproject.toml
* Add deptry config

## 0.5.7 - 2023-08-17

* Update column data type validator

## 0.5.6 - 2023-08-10

* Use latest version of certifi (2023.7.22)

## 0.5.5 - 2023-08-07

* Linting with flakeheaven

## 0.5.4 - 2023-08-01

* Add support for Looker's `Users Attributes`

## 0.5.3 - 2023-07-27

* Add support for PowerBI's `Activity Events`

## 0.5.2 - 2023-07-12

* Fix Metabase DbClient url

## 0.5.1 - 2023-07-03

* Add support for Looker's `ContentViews`

## 0.5.0 - 2023-06-28

* Stop supporting python3.7

## 0.4.1 - 2023-06-27

* Fix on Sigma elements extraction
* Fix BigQuery dataset extraction
* Fix the File Checker for View DDL file

## 0.4.0 - 2023-06-12

* Added support for Sigma

## 0.3.8 - 2023-05-02

* Added support for PowerBI datasets and fields

## 0.3.7 - 2023-04-28

* Warning message to deprecate python < 3.8

## 0.3.6 - 2023-04-24

* Update enum keys for Metabase credentials

## 0.3.5 - 2023-04-07

* Extract metadata from successful dbt runs only

## 0.3.4 - 2023-04-05

* Enhance uploader to support `QUALITY` files

## 0.3.3 - 2023-04-04

* Tableau : Improve Table <> Datasource lineage

## 0.3.2 - 2023-04-04

* Allow COPY statements from Snowflake

## 0.3.1 - 2023-03-30

* Improved Field extraction in Tableau

## 0.3.0 - 2023-03-29

* Added Tableau datasource and field integration

## 0.2.3 - 2023-03-17

* Verify required admin permissions for Looker extraction

## 0.2.2 - 2023-03-13

* Constrain `setuptools` explicitly added

## 0.2.1 - 2023-02-23

* Constrain `google-cloud-bigquery` dependency below yanked 3.0.0

## 0.2.0 - 2023-02-13

* Add connector for dbt-cloud

## 0.1.2 - 2023-02-08

* Enhance **Looker** extraction of dashboard filters and groups with roles

## 0.1.1 - 2023-02-06

* Add **Looker** support to extract `groups`-related assets
* Enhance **Looker** extraction of dashboard elements and users

## 0.1.0 - 2023-01-17

* Upgrade to Python 3.8
* Upgrade dependencies

## 0.0.44 - 2023-01-02

* Introduce new extractor for visualization tool **PowerBi** with support for
  * `reports`
  * `dashboards`
  * `metadata`

## 0.0.43 - 2022-12-21

* Update package dependencies

## 0.0.42 - 2022-11-25

* Improve pagination

## 0.0.41 - 2022-10-26

* Tableau: Optional `site-id` argument for Tableau Server users

## 0.0.40 - 2022-10-25

* Fix command `file_check`

## 0.0.39 - 2022-10-24

* Fix `FileChecker` template for `GenericWarehouse.view_ddl`

## 0.0.38 - 2022-10-17

* Snowflake: extract `warehouse_size`

## 0.0.37 - 2022-10-14

* Allow to skip "App size exceeded" error while fetching Qlik measures
* Fix missing arguments `warehouse` and `role` passing for script `extract_snowflake`

## 0.0.36 - 2022-10-13

* Patch error in Looker explore names

## 0.0.35 - 2022-10-12

* Add safe mode to **Looker**

## 0.0.34 - 2022-10-11

* Fix extras dependencies

## 0.0.33 - 2022-10-10

* Migrate package generation to poetry

## 0.0.32 - 2022-10-07

* Improved logging

## 0.0.31 - 2022-10-05

* Safe mode for bigquery and file logger

## 0.0.30 - 2022-09-20

* Add **Qlik** support to extract `connections` assets

## 0.0.29 - 2022-08-31

* Switch to engine's connect for database connections

## 0.0.28 - 2022-07-29

* Widen dependencies ranges

## 0.0.27 - 2022-07-28

* Improve support for Qlik `measures` and `lineage` and drop extraction of `qvds`

## 0.0.26 - 2022-07-22

* Add **Qlik** support to extract `measures` assets

## 0.0.25 - 2022-07-04

* Add **Qlik** support to extract `qvds` and `lineage` assets

## 0.0.24 - 2022-06-30

* Allow to use `all_looks` endpoint to retrieve looker Looks for param or env variable.

## 0.0.23 - 2022-06-29

* Allow to change Looker api timeout through param or env variable.

## 0.0.22 - 2022-06-20

* Introduce new extractor for visualization tool **Qlik** with support for
  * `spaces`
  * `users`
  * `apps`

## 0.0.21 - 2022-06-09

* Fix typo in Snowflake schema extract query

## 0.0.20 - 2022-06-08

* Fetch only distinct schemas in Snowflake warehouse

## 0.0.19 - 2022-05-30

* Use versions with range to ease dependency resolution for python 3.7 to 3.10

## 0.0.18 - 2022-05-19

* Enhance the file checker to search for prefixed files

## 0.0.17 - 2022-05-18

* Add retry for mode analytics

## 0.0.16 - 2022-05-18

* Add options to the pager:
  * `start_page`: to start pagination at another index (default to 1)
  * `stop_strategy`: to use different strategy to stop pagination (default to EMPTY_PAGE)

## 0.0.15 - 2022-05-09

* Skip snowflake columns with no name

## 0.0.14 - 2022-05-09

* Add missing metabase dependencies on Psycopg2

## 0.0.13 - 2022-05-06

* Remove top-level imports to isolate modules with different extra dependencies

## 0.0.12 - 2022-05-06

* Improved the file checker to detect repeated quotes in CSV.

## 0.0.11 - 2022-05-02

* Fix import error in `file_checker` script

## 0.0.10 - 2022-04-27

* Snowflake: discard 11 more `query_type` values when fetching queries

## 0.0.9 - 2022-04-13

* allow Looker parameters `CASTOR_LOOKER_TIMEOUT_SECOND` and `CASTOR_LOOKER_PAGE_SIZE` to be passed through environment
variables
* fix import paths in `castor_extractor/commands/upload.py` script
* use `storage.Client.from_service_account_info` when `credentials` is a dictionary in `uploader/upload.py`

## 0.0.8 - 2022-04-07

* Fix links to documentation in the README

## 0.0.7 - 2022-04-05

* Fix dateutil import issue

## 0.0.6 - 2022-04-05

First version of Castor Extractor, including:

* Warehouse assets extraction
  * BigQuery
  * Postgres
  * Redshift
  * Snowflake

* Visualization assets extraction
  * Looker
  * Metabase
  * Mode Analytics
  * Tableau

* Utilities
  * Uploader to cloud-storage
  * File Checker (for generic metadata)
