import click
from pydantic import BaseModel
from datetime import date
from typing import List

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
    id: str
        
class Sample(BaseModel):
    """
    Metadata describing the sample and sample preparation.
    """
    description: str
    protocol: str
    contributions: str

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

if __name__ == '__main__':
    main()