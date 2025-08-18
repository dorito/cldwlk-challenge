from sqlalchemy import MetaData
from app.config import Config
from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
  metadata = MetaData(schema=Config.DB_SCHEMA)