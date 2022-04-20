from typing import Optional, Sequence
from enum import Enum
from pydantic.color import Color
from sqlmodel import SQLModel
from .multiscale.cosem import SpatialTransform


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


class ContrastLimits(SQLModel):
    start: int
    end: int
    min: int
    max: int


class DisplaySettings(SQLModel):
    """
    Metadata for display settings
    """

    contrastLimits: ContrastLimits
    color: Color | None
    invertLUT: bool


class DataSource(SQLModel):
    """
    An abstract data source. Volume and mesh source metadata are
    derived from this interface.
    """
    name: str
    description: str
    url: str
    format: str
    transform: SpatialTransform


class MeshSource(DataSource, table=True):
    format: MeshTypeEnum
    ids: list[int]


class VolumeSource(DataSource, table=True):
    format: ArrayContainerTypeEnum
    sampleType: SampleTypeEnum
    contentType: ContentTypeEnum
    displaySettings: DisplaySettings
    subsources: list[MeshSource]
