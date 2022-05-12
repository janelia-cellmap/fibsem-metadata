from pydantic import Field
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
    institutions: list[str]
    software_availability: SoftwareAvailability
    acquisition: FIBSEMAcquisition | None
    sample: Sample | None
    publications: list[Publication]


class DatasetCreate(Dataset):
    pass

class DatasetRead(Dataset):
    id: int

class DatasetUpdate(Dataset):
    pass
