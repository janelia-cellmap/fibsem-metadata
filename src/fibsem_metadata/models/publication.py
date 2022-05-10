from .base import Base
from enum import Enum
from pydantic import HttpUrl


class PublicationTypeEnum(str, Enum):
    doi = "doi"
    paper = "paper"


class Publication(Base):
    name: str
    type: PublicationTypeEnum
    url: HttpUrl


class PublicationRead(Base):
    id: int