from .base import Base
from enum import Enum
from pydantic import HttpUrl

class PublicationTypeEnum(str, Enum):
    doi = "doi"
    paper = "paper"

class Hyperlink(Base):
    href: HttpUrl
    title: str

class Publication(Hyperlink):
    type: PublicationTypeEnum