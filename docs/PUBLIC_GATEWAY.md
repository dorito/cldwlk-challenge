# Public Gateway

## Description
- Service that can be accessed by external applications

## System overview
- Existing financial data history can added at the endpoint `/financial-transaction/new [POST]` 
  - The request must be authenticated, otherwise it'll fail
- Existing financial data history can be seen at the endpoint `/financial-transaction/list [GET]` 
  - The request must be authenticated, otherwise it'll fail
- Existing emotional data history can added at the endpoint `/emotion/new [POST]` 
  - The request must be authenticated, otherwise it'll fail
- Existing emotional data history can be seen at the endpoint `/emotion/list [GET]` 
  - The request must be authenticated, otherwise it'll fail
- Existing credit loan requests history can added at the endpoint `/credit-loan/new [POST]` 
  - The request must be authenticated, otherwise it'll fail
- Existing credit loan requests data history can be seen at the endpoint `/credit-loan/list [GET]` 
  - The request must be authenticated, otherwise it'll fail
- Health check endpoint can be accessed at `/internal/health [GET]`
  - It's only called from internal applications
- Users can be created at `/internal/tests/create-user [POST]`
  - It only exists to validate the other endpoints
- Users can get a valid api key at `/internal/tests/fetch-api-key [POST]`
  - It only exists to validate the other endpoints
- Asynchronous processing is made with Celery
- API is served with FastAPI

## Folders overview
- `app`: has files related to app core functionality (ex: configuration files and database migrations)
- `data`: has files related to data models (schemas, enums and database models)
- `services`: has files that make the system actions