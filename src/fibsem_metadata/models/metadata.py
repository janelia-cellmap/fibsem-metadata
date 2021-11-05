import click
from pydantic import BaseModel
from datetime import date
from typing import List, Dict
from enum import Enum


class SoftwareAvailability(str, Enum):
    open = "open"
    partial = "partially open"
    closed = "closed"


class UnitfulVector(BaseModel):
    unit: str
    values: Dict[str, float]


class ImagingMetadata(BaseModel):
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


class SampleMetadata(BaseModel):
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


class DOI(BaseModel):
    id: str
    DOI: str


class DatasetMetadata(BaseModel):
    """
    Metadata for a bioimaging dataset.
    """

    title: str
    id: str
    imaging: ImagingMetadata
    sample: SampleMetadata
    institution: List[str]
    softwareAvailability: SoftwareAvailability
    DOI: List[DOI]
    publications: List[str]


@click.command()
def main() -> None:
    click.echo(DatasetMetadata.schema_json(indent=2))


if __name__ == "__main__":
    main()
