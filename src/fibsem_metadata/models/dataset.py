from enum import Enum
from typing import List, Optional
from pydantic import HttpUrl

from .acquisition import FIBSEMAcquisition
from .base import Base
from .publication import Publication
from .sample import Sample
from .source import Image
from .view import View


class SoftwareAvailability(str, Enum):
    open = "open"
    partial = "partially open"
    closed = "closed"


class Dataset(Base):
    name: str
    description: str
    institutions: List[str]
    softwareAvailability: SoftwareAvailability
    acquisition: Optional[FIBSEMAcquisition]
    sample: Optional[Sample]
    publications: List[Publication]
    images: List[Image]
    views: List[View]
    thumbnailURL: HttpUrl


class DatasetCreate(Dataset):
    pass


class DatasetRead(Dataset):
    id: int


class DatasetUpdate(Dataset):
    pass
