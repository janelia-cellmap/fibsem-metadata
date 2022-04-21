from sqlalchemy import String
from sqlalchemy.dialects import postgresql
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from datetime import date
from typing import TYPE_CHECKING, Any
from enum import Enum
from pydantic import HttpUrl

if TYPE_CHECKING:
    from .views import View


class SoftwareAvailability(str, Enum):
    open = "open"
    partial = "partially open"
    closed = "closed"


class Hyperlink(SQLModel):
    href: HttpUrl
    title: str


class UnitfulVector(SQLModel):
    unit: str
    values: dict[str, float]


class DOI(SQLModel):
    name: str
    doi: str


class ImageAcquisition(SQLModel):
    instrument: str
    institution: str
    startDate: date
    gridSpacing: UnitfulVector
    dimensions: UnitfulVector


class FIBSEMAcquisitionBase(ImageAcquisition):
    """
    Metadata describing the FIB-SEM imaging process.
    """
    duration_days: int | None
    biasVoltage: float | None
    scanRate: float | None
    current: float | None
    primaryEnergy: float | None


class FIBSEMAcquisition(FIBSEMAcquisitionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    gridSpacing: dict[str, Any] = Field(sa_column=Column(JSON))
    dimensions: dict[str, Any] = Field(sa_column=Column(JSON))

class DummyChild(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    acquistion_id: int | None = Field(foreign_key="fibsemacquisition.id")
    acquisition: FIBSEMAcquisition | None = Relationship()

class SampleBase(SQLModel):
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
    institution: list[str]


class Sample(SampleBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    organism: list[str] = Field(sa_column=Column(postgresql.ARRAY(String)))
    type: list[str] = Field(sa_column=Column(postgresql.ARRAY(String)))
    subtype: list[str] = Field(sa_column=Column(postgresql.ARRAY(String)))
    treatment: list[str] = Field(sa_column=Column(postgresql.ARRAY(String)))
    institution: list[str] = Field(sa_column=Column(postgresql.ARRAY(String)))


class DatasetBase(SQLModel):
    """
    Metadata for a bioimaging dataset.
    """

    name: str
    description: str
    #acquisition: FIBSEMAcquisition | None
    #sample: Sample
    views: list["View"] = Relationship(back_populates="dataset")
    institution: list[str]
    softwareAvailability: SoftwareAvailability
    doi: list[Hyperlink | DOI]
    publications: list[Hyperlink]


class Dataset(DatasetBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    institution: list[str] = Field(sa_column=Column(postgresql.ARRAY(String)))
    #acquisition_id: int | None = Field(default=None, foreign_key="FIBSEMAcquisition.id")
    #acquisition: FIBSEMAcquisition | None = Relationship()
    doi: list[Hyperlink | DOI] = Field(sa_column=Column(postgresql.JSONB))
    publications: list[Hyperlink] = Field(sa_column=Column(postgresql.JSONB))