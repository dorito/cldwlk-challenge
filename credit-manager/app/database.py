from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

from app.config import Config

ENGINE = create_engine(Config.SQLALCHEMY_URI, poolclass=NullPool)
DbSession = scoped_session(sessionmaker(autoflush=True))


def init_db_session():
    DbSession.configure(bind=ENGINE)
