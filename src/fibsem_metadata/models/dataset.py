from .sample import Sample
from .acquisition import FIBSEMAcquisition
from .base import Base
from enum import Enum
from datetime import date
from .source import Volume
from .view import View
from .publication import Publication


class SoftwareAvailability(str, Enum):
    open = "open"
    partial = "partially open"
    closed = "closed"


class Dataset(Base):
    name: str
    description: str
    institution: list[str]
    softwareAvailability: SoftwareAvailability
    acquisition: FIBSEMAcquisition
    sample: Sample
    publications: list[Publication]
    volumes = list[Volume]
    views = list[View]
