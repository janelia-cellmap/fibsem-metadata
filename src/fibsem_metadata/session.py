from typing import Generator
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .schemas.base import Base
from pydantic.json import pydantic_encoder
import json

def json_serializer(*args, **kwargs) -> str:
    return json.dumps(*args, default=pydantic_encoder, **kwargs)

db_url = "postgresql://admin:admin@localhost:5432/fibsem_metadata"


engine = create_engine(db_url, future=True, echo=True, json_serializer=json_serializer)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db_and_tables(engine, wipe=False):
    if wipe:
        Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)
