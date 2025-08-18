from app.config import Config
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    metadata = MetaData(schema=Config.DB_SCHEMA)
