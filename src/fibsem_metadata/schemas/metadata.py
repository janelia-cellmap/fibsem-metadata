from datetime import date
from typing import List, Dict, Union
from enum import Enum

from .base import StrictBaseModel
from pydantic import HttpUrl


class Hyperlink(StrictBaseModel):
    href: HttpUrl
    title: str


class SoftwareAvailability(str, Enum):
    open = "open"
    partial = "partially open"
    closed = "closed"


class UnitfulVector(StrictBaseModel):
    unit: str
    values: Dict[str, float]


class ImageAcquisition(StrictBaseModel):
    name: str
    institution: str
    gridSpacing: UnitfulVector
    dimensions: UnitfulVector


class FIBSEMAcquisition(ImageAcquisition):
    """
    Metadata describing the FIB-SEM imaging process.
    """

    startDate: date
    duration: int
    biasVoltage: float
    scanRate: float
    current: float
    primaryEnergy: float


class Sample(StrictBaseModel):
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
    name: str
    doi: str


class Dataset(StrictBaseModel):
    """
    Metadata for a bioimaging dataset.
    """

    title: str
    id: str
    imaging: FIBSEMAcquisition
    sample: Sample
    institution: List[str]
    softwareAvailability: SoftwareAvailability
    doi: List[Union[Hyperlink, DOI]]
    publications: List[Union[Hyperlink, str]]
