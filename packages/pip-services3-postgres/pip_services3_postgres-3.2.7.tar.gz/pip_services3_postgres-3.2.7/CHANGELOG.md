# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> PostgreSQL components for Python Changelog

## <a name="3.2.7"></a> 3.2.7 (2023-10-31)

### Bug fixed
* Fixed bug with `_quote_identifier` schema builder

## <a name="3.2.6"></a> 3.2.6 (2022-07-21)

### Bug fixed
* Added wrapping try finally for requests

## <a name="3.2.5"></a> 3.2.5 (2021-11-25)

### Bug fixed
* Fixed PostgresPersistence filter methods

## <a name="3.2.4"></a> 3.2.4 (2021-10-29)

### Bug fixed
* Fixed IdentifiablePostgresPersistence.set method

## <a name="3.2.3"></a> 3.2.3 (2021-10-28)

### Bug fixes
* Optimized imports
* Updated requirements

## <a name="3.2.2"></a> 3.2.2 (2021-09-02)

### Features
* Replace psycopg2 on psycopg2-binary dependency for AWS lambda deploy

## <a name="3.2.1"></a> 3.2.1 (2021-08-25)

### Features
* Added _request method for PostgresPersistence

## <a name="3.2.0"></a> 3.2.0 (2021-08-06)

Added support for SQL schemas

### Features
* Added schema support to PostgresPersistence, IdentifiablePostgresPersistenve, IdentifiableJsonPostgresPersistence
* Added _auto_generate_id flag to IdentifiableSqlServerPersistence

## <a name="3.1.0"></a> 3.1.0 (2021-05-14)

### Bug Fixes
* fix private, protected method names
* Fixed returned types for operations

### Features
* Moved PostgresConnection to **connect** package
* Added type hints

## <a name="3.0.0"></a> 3.0.0 (2021-03-12) 

Initial public release

### Features
* Added DefaultPostgresFactory
* Added PostgresConnectionResolver
* Added IdentifiableJsonPostgresPersistence
* Added IdentifiablePostgresPersistence
* Added IdentifiablePostgresPersistence
* Added PostgresPersistence