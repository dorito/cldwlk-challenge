import os
import urllib.parse
from dataclasses import dataclass


@dataclass
class Config:
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_NAME: str = os.getenv("APP_NAME")
    CELERY_BROKER: str = os.getenv("CELERY_BROKER")
    CELERY_BACKEND: str = os.getenv("CELERY_BACKEND")
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_FINANCIAL_TRANSACTION_TOPIC: str = "FINANCIAL_TRANSACTION_DATA"
    KAFKA_EMOTIONAL_TOPIC_NAME: str = "EMOTIONAL_DATA"
    EMOTION_PROCESSOR_LIST_TRACE_ENDPOINT: str = os.getenv("EMOTION_PROCESSOR_LIST_TRACE_ENDPOINT", "http://emotion-processor-api/internal/emotion-trace-data/by-profile-guid/")
    CREDIT_MANAGER_FINANCIAL_TRANSACTION_LIST_ENDPOINT: str = os.getenv("FINANCIAL_TRANSACTION_LIST_ENDPOINT", "http://credit-manager-api/internal/financial-transaction-data/by-profile-guid/")
    CREDIT_MANAGER_CREDIT_REQUEST_CREATE_ENDPOINT: str = os.getenv("CREDIT_REQUEST_CREATE_ENDPOINT", "http://credit-manager-api/internal/credit-request")
    CREDIT_MANAGER_CREDIT_REQUEST_LIST_ENDPOINT: str = os.getenv("CREDIT_REQUEST_LIST_ENDPOINT", "http://credit-manager-api/internal/credit-request/by-profile-guid/")
    KAFKA_GROUP_ID: str = "public-gateway-group"
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT"))
    DB_SCHEMA: str = os.getenv("DB_SCHEMA")
    SQLALCHEMY_URI: str = f"postgresql+psycopg2://{DB_USER}:{urllib.parse.quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
