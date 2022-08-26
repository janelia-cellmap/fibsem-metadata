import json
from typing import Any, Callable

from pydantic.json import pydantic_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from fibsem_metadata.core.config import settings

SessionLocal: Callable[[], Session]


def json_serializer(*args: Any, **kwargs: Any) -> str:
    return json.dumps(*args, default=pydantic_encoder, **kwargs)


engine = create_engine(
    settings.db_uri(),
    future=True,
    echo=True,
    json_serializer=json_serializer,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
