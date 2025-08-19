# Emotion Processor

## Description
- Service that saves emotion data history

## System overview
- New emotion data comes from a kafka topic (`EMOTIONAL_DATA`) and are processed at `emotion-processor-kafka-worker`
- Existing emotion data history can be seen at the endpoint `/internal/emotion-trace-data/by-profile-guid/{user_profile_guid}` 
  - It's only called from internal applications
- Health check endpoint can be accessed at `/internal/health [GET]`
  - It's only called from internal applications
- Asynchronous processing is made with Celery and are processed at `emotion-processor-queue-worker`
- API is served with FastAPI at `emotion-processor-api`

## Folders overview
- `app`: has files related to app core functionality (ex: configuration files and database migrations)
- `data`: has files related to data models (schemas, enums and database models)
- `services`: has files that make the system actions
- `tasks`: has files with asynchronous jobs