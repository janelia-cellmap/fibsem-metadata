from datetime import date
from .base import Base


class UnitfulVector(Base):
    unit: str
    values: dict[str, float]


class ImageAcquisition(Base):
    id: str
    institution: str
    gridSpacing: UnitfulVector
    dimensions: UnitfulVector


class FIBSEMAcquisition(ImageAcquisition):
    """
    Metadata describing the FIB-SEM imaging process.
    """

    startDate: date
    duration: int
    biasVoltage: float
    scanRate: float
    current: float
    primaryEnergy: float
