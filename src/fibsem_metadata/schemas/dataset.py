from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
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

    images = relationship(
        ImageTable, cascade="all, delete-orphan", passive_deletes=True
    )
    views = relationship(ViewTable, cascade="all, delete-orphan", passive_deletes=True)

    acquisition_id = Column(
        Integer,
        ForeignKey("fibsem_acquisition.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    acquisition = relationship(FIBSEMAcquisitionTable, back_populates="datasets")

    sample_id = Column(
        Integer, ForeignKey("sample.id", ondelete="CASCADE"), nullable=True, index=True
    )

    sample = relationship(SampleTable, back_populates="datasets")

    publications = relationship(
        PublicationTable, secondary=pub_to_dataset, back_populates="datasets"
    )
    published = Column(Boolean, nullable=False)
    thumbnail_url = Column(String)
