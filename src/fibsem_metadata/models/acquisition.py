from datetime import date
from datetime import date
from pydantic import Json
from .base import Base


class UnitfulVector(Base):
    unit: str
    values: dict[str, float]


class ImageAcquisition(Base):
    name: str
    institution: str
    start_date: date | None
    grid_spacing: UnitfulVector
    dimensions: UnitfulVector


class FIBSEMAcquisition(ImageAcquisition):
    """
    Metadata describing the FIB-SEM imaging process.
    """

    start_date: date | None
    duration_days: int | None
    bias_voltage: float | None
    scan_rate: float | None
    current: float | None
    primary_energy: float | None


class FIBSEMAcquisitionRead(FIBSEMAcquisition):
    id: int