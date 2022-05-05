from .base import Base
from .source import VolumeTable
from .view import ViewTable
from .acquisition import FIBSEMAcquisitionTable
from .sample import SampleTable
from .publication import PublicationTable, pub_to_dataset
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql


class DatasetTable(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    description = Column(String)

    institution = Column(postgresql.ARRAY(String))
    software_availability = Column(String)

    volumes = relationship(VolumeTable, back_populates="dataset")
    views = relationship(ViewTable, back_populates="dataset")
    acquisition_id = Column(
        Integer, ForeignKey("fibsem_acquisition.id"), nullable=False
    )
    acquisition = relationship(FIBSEMAcquisitionTable, back_populates="datasets")

    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    sample = relationship(SampleTable, back_populates="datasets")

    publications = relationship(
        PublicationTable, secondary=pub_to_dataset, back_populates="datasets"
    )
