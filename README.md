# Coding Challenge Solution

Here is my solution to the proposed coding challenge.

## Project overview
- Each application communicates with each other using Kafka, in an event driven architecture
- Each application that have asynchronous processing does so using Celery
- Each application that have public endpoints does so using FastAPI
- For all applications, PostgreSQL is used for database and Redis is used for cache

## How to start the project in my machine
You need to have `docker` installed and accessible by your terminal. With it, you can run the following command in the root folder to start the project:
- `docker compose up -d`

If you need to change any port of services that use them in the host machine, please populate the `.env` file, using `.env.example` as base for this.