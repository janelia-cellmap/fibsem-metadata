from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from .acquisition import FIBSEMAcquisitionTable
from .base import Base
from .publication import PublicationTable, pub_to_dataset
from .sample import SampleTable
from .source import ImageTable
from .view import ViewTable


class DatasetTable(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    institutions = Column(postgresql.ARRAY(String))
    software_availability = Column(String)

    images = relationship(ImageTable)
    views = relationship(ViewTable)

    acquisition_id = Column(
        Integer, ForeignKey("fibsem_acquisition.id"), nullable=True, index=True
    )

    acquisition = relationship(FIBSEMAcquisitionTable, back_populates="datasets")

    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=True, index=True)

    sample = relationship(SampleTable, back_populates="datasets")

    publications = relationship(
        PublicationTable, secondary=pub_to_dataset, back_populates="datasets"
    )
