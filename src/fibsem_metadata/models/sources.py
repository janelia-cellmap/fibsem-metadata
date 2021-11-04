from typing import Optional, Sequence
from enum import Enum
from pydantic import BaseModel
from pydantic.color import Color
from fibsem_metadata.models.multiscale.cosem import SpatialTransform


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
    mrc = "mrc"
    hdf5 = "hdf5"
    tif = "tif"


class ContentTypeEnum(str, Enum):
    em = "em"
    lm = "lm"
    prediction = "prediction"
    segmentation = "segmentation"
    analysis = "analysis"


class SampleTypeEnum(str, Enum):
    scalar = "scalar"
    label = "label"


class ContrastLimits(BaseModel):
    start: int
    end: int
    min: int
    max: int


class DisplaySettings(BaseModel):
    """
    Metadata for display settings
    """

    contrastLimits: ContrastLimits
    color: Optional[Color]
    invertLUT: bool


class DataSource(BaseModel):
    name: str
    description: str
    URI: str
    format: str
    transform: SpatialTransform


class MeshSource(DataSource):
    format: MeshTypeEnum
    ids: Sequence[int]


class VolumeSource(DataSource):
    format: ArrayContainerTypeEnum
    sampleType: SampleTypeEnum
    contentType: ContentTypeEnum
    displaySettings: DisplaySettings
    subsources: Sequence[MeshSource] = []
