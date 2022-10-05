from enum import Enum

from pydantic import HttpUrl

from .base import Base


class PublicationType(str, Enum):
    """
    The types of publications supported -- DOI or paper.
    """

    doi = "doi"
    paper = "paper"


class Publication(Base):
    name: str
    type: PublicationType
    url: HttpUrl


class PublicationRead(Base):
    id: int
