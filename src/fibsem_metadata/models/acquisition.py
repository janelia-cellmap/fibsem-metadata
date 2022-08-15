from datetime import date
from typing import Dict, Optional
from .base import Base


class UnitfulVector(Base):
    unit: str
    values: Dict[str, float]


class ImageAcquisition(Base):
    name: str
    institution: str
    start_date: Optional[date]
    grid_spacing: UnitfulVector
    dimensions: UnitfulVector


class FIBSEMAcquisition(ImageAcquisition):
    """
    Metadata describing the FIB-SEM imaging process.
    """

    start_date: Optional[date]
    duration_days: Optional[int]
    bias_voltage: Optional[float]
    scan_rate: Optional[float]
    current: Optional[float]
    primary_energy: Optional[float]


class FIBSEMAcquisitionRead(FIBSEMAcquisition):
    id: int
