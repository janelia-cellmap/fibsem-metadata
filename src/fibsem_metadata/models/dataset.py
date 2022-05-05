from .base import Base
from enum import Enum
from pydantic import HttpUrl
from datetime import date
from .sources import Volume
from .views import View

class SoftwareAvailability(str, Enum):
    open = "open"
    partial = "partially open"
    closed = "closed"

class PublicationTypeEnum(str, Enum):
    doi = "doi"
    paper = "paper"

class Hyperlink(Base):
    href: HttpUrl
    title: str

class Publication(Hyperlink):
    type: PublicationTypeEnum

class UnitfulVector(Base):
    unit: str
    values: dict[str, float]


class ImagingMetadata(Base):
    id: str
    institution: str
    gridSpacing: UnitfulVector
    dimensions: UnitfulVector


class FIBSEMImagingMetadata(ImagingMetadata):
    """
    Metadata describing the FIB-SEM imaging process.
    """

    startDate: date
    duration: int
    biasVoltage: float
    scanRate: float
    current: float
    primaryEnergy: float


class SampleMetadata(Base):
    """
    Metadata describing the sample and sample preparation.
    """

    description: str
    protocol: str
    contributions: str
    organism: list[str]
    type: list[str]
    subtype: list[str]
    treatment: list[str]


class Dataset(Base):
    name: str
    description: str
    institution: list[str]
    softwareAvailability: SoftwareAvailability
    acquisition: FIBSEMImagingMetadata
    sample: SampleMetadata
    publications: list[Publication]
    volumes = list[Volume]
    views = list[View]