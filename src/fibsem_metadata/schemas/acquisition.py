from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from .base import Base


class ImageAcquisitionMixin:
    name = Column(String)
    instrument = Column(String)
    institution = Column(String)
    start_date = Column(Date)
    grid_spacing = Column(postgresql.JSONB)
    dimensions = Column(postgresql.JSONB)


class FIBSEMAcquisitionTable(Base, ImageAcquisitionMixin):
    __tablename__ = "fibsem_acquisition"

    id = Column(Integer, primary_key=True, autoincrement=True)
    duration_days = Column(Integer)
    bias_voltage = Column(Float)
    scan_rate = Column(Float)
    current = Column(Float)
    primary_energy = Column(Float)
    datasets = relationship("DatasetTable", cascade="all, delete-orphan")
