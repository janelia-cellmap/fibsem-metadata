from datetime import date
from typing import Dict, Optional

from .base import Base


class UnitfulVector(Base):
    unit: str
    values: Dict[str, float]


class ImageAcquisition(Base):
    name: str
    institution: str
    startDate: Optional[date]
    gridSpacing: UnitfulVector
    dimensions: UnitfulVector


class FIBSEMAcquisition(ImageAcquisition):
    """
    Metadata describing the FIB-SEM imaging process.
    """

    startDate: Optional[date]
    durationDays: Optional[int]
    biasVoltage: Optional[float]
    scanRate: Optional[float]
    current: Optional[float]
    primaryEnergy: Optional[float]


class FIBSEMAcquisitionRead(FIBSEMAcquisition):
    id: int
