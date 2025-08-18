from sqlalchemy import create_engine
from app.config import Config
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine(
    Config.SQLALCHEMY_URI, poolclass=NullPool
)
SESSION = scoped_session(sessionmaker(autoflush=True))

def init_db_session():
    SESSION.configure(bind=engine)