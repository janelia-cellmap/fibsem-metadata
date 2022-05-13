from pydantic import PositiveInt
from ..base import Base


class PixelResolution(Base):
    """
    PixelResolution attribute used by the saalfeld lab.
    The dimensions attribute contains a list of scales that define the
    grid spacing of the data, in F-order.
    """

    dimensions: list[float]
    unit: str


# todo: validate argument lengths
class NeuroglancerN5GroupMetadata(Base):
    """
    Metadata to enable displaying an N5 group containing several datasets
    as a multiresolution dataset in neuroglancer. See
    https://github.com/google/neuroglancer/issues/176#issuecomment-553027775
    Axis properties are in F-order.
    """

    axes: list[str]
    units: list[str]
    scales: list[list[PositiveInt]]
    pixelResolution: PixelResolution
