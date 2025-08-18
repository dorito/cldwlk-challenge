import os
import urllib.parse
from dataclasses import dataclass


@dataclass
class Config:
    APP_ENV: str = os.getenv("APP_ENV", "development")
    CELERY_BROKER: str = os.getenv("CELERY_BROKER")
    CELERY_BACKEND: str = os.getenv("CELERY_BACKEND")
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_EMOTIONAL_TOPIC_NAME: str = "EMOTIONAL_DATA"
    KAFKA_GROUP_ID: str = "emotional-processor-group"
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT"))
    DB_SCHEMA: str = os.getenv("DB_SCHEMA")
    SQLALCHEMY_URI: str = f"postgresql+psycopg2://{DB_USER}:{urllib.parse.quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
