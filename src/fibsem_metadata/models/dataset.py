import click
from pydantic import BaseModel
from datetime import date
from typing import List, Dict


class UnitfulVector(BaseModel):
    unit: str
    values: Dict[str, float]


class Imaging(BaseModel):
    """
    Metadata describing the FIB-SEM imaging process.
    """

    startDate: date
    duration: int
    biasVoltage: float
    scanRate: float
    current: float
    primaryEnergy: float
    gridSpacing: UnitfulVector
    dimensions: UnitfulVector
    id: str


class Sample(BaseModel):
    """
    Metadata describing the sample and sample preparation.
    """

    description: str
    protocol: str
    contributions: str
    organism: str
    type: str
    subtype: str
    treatment: str


class DOI(BaseModel):
    id: str
    DOI: str


class Dataset(BaseModel):
    """
    Metadata for a FIB-SEM dataset.
    """

    title: str
    id: str
    publications: List[str] = []
    imaging: Imaging
    sample: Sample
    DOI: List[DOI]


@click.command()
def main() -> None:
    print(Dataset.schema_json(indent=2))


if __name__ == "__main__":
    main()
