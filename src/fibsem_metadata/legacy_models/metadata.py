from datetime import date
from typing import List, Dict, Union
from enum import Enum

from fibsem_metadata.legacy_models.base import StrictBaseModel
from pydantic import HttpUrl
from .sources import VolumeSource
from .views import DatasetView


class SoftwareAvailability(str, Enum):
    open = "open"
    partial = "partially open"
    closed = "closed"


class PublicationTypeEnum(str, Enum):
    doi = "doi"
    paper = "paper"


class Hyperlink(StrictBaseModel):
    href: HttpUrl
    title: str


class Publication(Hyperlink):
    type: PublicationTypeEnum


class UnitfulVector(StrictBaseModel):
    unit: str
    values: Dict[str, float]


class ImagingMetadata(StrictBaseModel):
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


class SampleMetadata(StrictBaseModel):
    """
    Metadata describing the sample and sample preparation.
    """

    description: str
    protocol: str
    contributions: str
    organism: List[str]
    type: List[str]
    subtype: List[str]
    treatment: List[str]


class DOI(StrictBaseModel):
    id: str
    DOI: str


class DatasetMetadata(StrictBaseModel):
    """
    Metadata for a bioimaging dataset.
    """

    title: str
    id: str
    imaging: FIBSEMImagingMetadata
    sample: SampleMetadata
    institution: List[str]
    softwareAvailability: SoftwareAvailability
    DOI: List[Union[Hyperlink, DOI]]
    publications: List[Union[Hyperlink, str]]


class Dataset(StrictBaseModel):
    name: str
    description: str
    institution: List[str]
    softwareAvailability: SoftwareAvailability
    acquisition: FIBSEMImagingMetadata
    sample: SampleMetadata
    publications: List[Publication]
    volumes: List[VolumeSource]
    views: List[DatasetView]
