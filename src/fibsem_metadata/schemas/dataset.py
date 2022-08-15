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
    name = Column(String, unique=True, index=True)
    description = Column(String)

    institutions = Column(postgresql.ARRAY(String))
    software_availability = Column(String)

    volumes = relationship(VolumeTable, lazy="selectin")
    views = relationship(ViewTable, lazy="selectin")

    acquisition_id = Column(
        Integer, ForeignKey("fibsem_acquisition.id"), nullable=True, index=True
    )

    acquisition = relationship(
        FIBSEMAcquisitionTable, back_populates="datasets", lazy="selectin"
    )

    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=True, index=True)

    sample = relationship(SampleTable, back_populates="datasets", lazy="selectin")

    publications = relationship(
        PublicationTable, secondary=pub_to_dataset, back_populates="datasets"
    )
