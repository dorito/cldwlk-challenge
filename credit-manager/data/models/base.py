from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.config import Config


class BaseModel(DeclarativeBase):
    metadata = MetaData(schema=Config.DB_SCHEMA)
