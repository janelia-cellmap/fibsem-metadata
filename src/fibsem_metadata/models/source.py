from typing import Optional, Sequence
from enum import Enum
from pydantic.color import Color
from .base import Base
from .source import Mesh
from fibsem_metadata.legacy_models.multiscale.cosem import SpatialTransform


class MeshTypeEnum(str, Enum):
    """
    Strings representing supported mesh formats
    """

    neuroglancer_legacy_mesh = "neuroglancer_legacy_mesh"
    neuroglancer_multilod_draco = "neuroglancer_multilod_draco"


class ArrayContainerTypeEnum(str, Enum):
    n5 = "n5"
    zarr = "zarr"
    precomputed = "precomputed"


class ContentTypeEnum(str, Enum):
    em = "em"
    lm = "lm"
    prediction = "prediction"
    segmentation = "segmentation"
    analysis = "analysis"


class SampleTypeEnum(str, Enum):
    scalar = "scalar"
    label = "label"


class ContrastLimits(Base):
    start: int
    end: int
    min: int
    max: int


class DisplaySettings(Base):
    """
    Metadata for display settings
    """

    contrastLimits: ContrastLimits
    color: Optional[Color]
    invertLUT: bool


class DataSource(Base):
    name: str
    description: str
    url: str
    format: str
    transform: SpatialTransform


class Mesh(DataSource):
    format: MeshTypeEnum
    ids: Sequence[int]


class Volume(DataSource):
    format: ArrayContainerTypeEnum
    sampleType: SampleTypeEnum
    contentType: ContentTypeEnum
    displaySettings: DisplaySettings
    subsources: list[Mesh]
