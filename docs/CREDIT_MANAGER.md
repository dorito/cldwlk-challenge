# Credit Manager

## Description
- Service that manages the credit loan requests and saves the financial transaction history

## System overview
- New financial transaction data comes from a kafka topic (`FINANCIAL_TRANSACTION_DATA`) and are processed at `credit-manager-kafka-worker`
- New credit loan requests comes from calls at the endpoint `/internal/credit-request [POST]`
  - It's only called from internal applications
- Existing loan requests can be seen at the endpoint `/internal/credit-request/by-profile-guid/{user_profile_guid} [GET]`
  - It's only called from internal applications
- Existing financial transactions can be seen at the endpoint `/internal/financial-transaction-data/by-profile-guid/{user_profile_guid} [GET]`
  - It's only called from internal applications
- Health check endpoint can be accessed at `/internal/health [GET]`
  - It's only called from internal applications
- Asynchronous processing is made with Celery and are processed at `credit-manager-queue-worker`
- API is served with FastAPI at `credit-manager-api`

## Folders overview
- `app`: has files related to app core functionality (ex: configuration files and database migrations)
- `data`: has files related to data models (schemas, enums and database models)
- `services`: has files that make the system actions
- `tasks`: has files with asynchronous jobs