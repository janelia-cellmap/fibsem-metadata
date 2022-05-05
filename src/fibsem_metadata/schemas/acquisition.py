from sqlalchemy import Column, Integer, relationship, Float, String, Date
from sqlalchemy.dialects import postgresql
from .base import Base


class ImageAcquisitionMixin:
    instrument = Column(String)
    institution = Column(String)
    start_date = Column(Date)
    sampling_grid_unit = Column(String)
    sampling_grid_spacing = Column(postgresql.ARRAY(Float))
    sampling_grid_shape = Column(postgresql.ARRAY(Integer))


class FIBSEMAcquisitionTable(Base, ImageAcquisitionMixin):
    __tablename__ = "fibsem_acquisition"

    id = Column(Integer, primary_key=True, autoincrement=True)
    duration_days = Column(Integer)
    bias_voltage = Column(Float)
    scan_rate = Column(Float)
    current = Column(Float)
    primary_energy = Column(Float)
    datasets = relationship("DatasetTable")
