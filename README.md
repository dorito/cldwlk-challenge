# Coding Challenge Solution

Here is my solution to the proposed coding challenge.

## Project overview
- Each application communicates with each other using Kafka, in an event driven architecture
- Each application that have asynchronous processing does so using Celery
- Each application that have public endpoints does so using FastAPI
- For all applications, PostgreSQL is used for database and Redis is used for cache

## How to start the project in your machine
You need to have `docker` installed and accessible by your terminal. With it, you can run the following command in the root folder to start the project:
- `docker compose up -d`

If you need to change any port of services that use them in the host machine, please populate the `.env` file, using `.env.example` as base for this.

## Base structure of each application
- All applications have at least a kafka-worker and a queue-worker container
- `credit-manager` and `user-manager` have an api container in addition of those two workers
- The `kafka-worker` containers focuses on consuming kafka topics, and dispatching jobs to further processing
  - For this, it uses the `kafka-python` library
- The `queue-worker` containers does the async processing (and with this, does most of the database / external resource calls)
  - For this, it uses the `celery` and `sqlalchemy` libraries
- The api containers uses `FastAPI` for serving the endpoints
- Every project has some (or all) of the following folders, each one containing the following type of files:
  - `app` - core functions and configs
  - `enums` - enums
  - `models` - models used for database retrieval/saving
  - `schemas` - schemas used for serializing/unserializing messages between services
  - `services` - app logic
  - `tasks` - asynchronous tasks
  - `tests` - unit tests
- The health check can be done by command, calling the `health_check.py` file and passing the `--service` that must be checked on (there are examples of this in the docker-compose.yaml files)
