from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import PositiveInt, root_validator, validator
from pydantic.color import Color

from .base import Base


class PixelResolution(Base):
    """
    PixelResolution attribute used by the saalfeld lab.
    The dimensions attribute contains a list of scales that define the
    grid spacing of the data, in F-order.
    """

    dimensions: List[float]
    unit: str


# todo: validate argument lengths
class NeuroglancerN5GroupMetadata(Base):
    """
    Metadata to enable displaying an N5 group containing several datasets
    as a multiresolution dataset in neuroglancer. See
    https://github.com/google/neuroglancer/issues/176#issuecomment-553027775
    Axis properties are in F-order.
    """

    axes: List[str]
    units: List[str]
    scales: List[List[PositiveInt]]
    pixelResolution: PixelResolution


class ScaleTranslate(Base):
    axes: List[str]
    units: List[Any]
    translate: List[Any]
    scale: List[Any]

    @root_validator
    def validate_argument_length(
        cls: "ScaleTranslate", values: Dict[str, Union[List[str], List[float]]]
    ) -> Dict[str, Union[List[str], List[float]]]:
        scale = values["scale"]
        axes = values["axes"]
        units = values["units"]
        translate = values["translate"]
        if not len(axes) == len(units) == len(translate) == len(scale):
            raise ValueError(
                f"The length of all arguments must match. {len(axes) = },  {len(units) = }, {len(translate) = }, {len(scale) = }"
            )
        return values


class OffsetTransform(ScaleTranslate):
    """
    A transform representing the intrinsic array-indexing-based space of
    N-dimensional arrays. For each axis, the axis name must be a the string
    representation of an integer starting from 0, the unit must be 'indices',
    the scale must be 1, and the offset must be an integer.
    """

    units: List[Literal["indices"]]
    translate: List[int]
    scale: List[Literal[1]]

    @validator("axes")
    def axes_must_be_stringed_ints(cls, v: List[str]):
        for idx, element in enumerate(v):
            if element != str(idx):
                raise ValueError(
                    f'Invalid axis name. Got {element}, expected "{str(idx)}"'
                )


class SpatialTransform(ScaleTranslate):
    """
    Representation of an N-dimensional scaling + translation transform for labelled axes with units.
    """

    units: List[str]
    translate: List[float]
    scale: List[float]


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

    contrast_limits: ContrastLimits
    color: Optional[Color]
    invert_lut: bool


class DataSource(Base):
    name: str
    description: str
    url: str
    format: str
    transform: SpatialTransform


class Mesh(DataSource):
    format: MeshTypeEnum
    ids: List[int]


class MeshRead(Mesh):
    id: int


class MeshCreate(Mesh):
    pass


class MeshUpdate(Mesh):
    pass


class Volume(DataSource):
    format: ArrayContainerTypeEnum
    sample_type: SampleTypeEnum
    content_type: ContentTypeEnum
    display_settings: DisplaySettings
    subsources: List[Mesh]


class VolumeRead(Volume):
    id: int


class VolumeCreate(Volume):
    pass


class VolumeUpdate(Volume):
    pass