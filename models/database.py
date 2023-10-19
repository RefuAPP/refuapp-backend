from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from configuration.config import Configuration
from configuration.database import (
    DatabaseName,
    DatabaseUser,
    DatabasePassword,
    DatabasePort,
    DatabaseHost,
)

db_name = Configuration.get(DatabaseName)
user = Configuration.get(DatabaseUser)
password = Configuration.get(DatabasePassword)
port = Configuration.get(DatabasePort)
host = Configuration.get(DatabaseHost)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
