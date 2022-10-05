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
    Representation of an N-dimensional scaling + translation transform for
    labelled axes with units.
    """

    units: List[str]
    translate: List[float]
    scale: List[float]


class MeshFormat(str, Enum):
    """
    Supported mesh formats
    """

    neuroglancer_legacy_mesh = "neuroglancer_legacy_mesh"
    neuroglancer_multilod_draco = "neuroglancer_multilod_draco"


class ArrayContainerFormat(str, Enum):
    """
    Supported chunked array container formats
    """
    n5 = "n5"
    zarr = "zarr"
    precomputed = "precomputed"


class ContentType(str, Enum):
    """
    Semantic classes for image data
    """
    em = "em"
    lm = "lm"
    prediction = "prediction"
    segmentation = "segmentation"
    analysis = "analysis"


class SampleType(str, Enum):
    """
    Semantic classes for image samples.
    The class "scalar" contains samples that represent a quantity.
    The class "label" contains samples that represent a class or identity.
    """
    scalar = "scalar"
    label = "label"


class ContrastLimits(Base):
    """
    Specifies the range of values to use when displaying an image.
    The "start" and "end" properties determine the values that should be
    mapped to the lowest and highest intensities in a given lookup table.

    The "min" and "max" values determine the lowest and highest possible
    values in the image histogram. These values are useful to setting up
    the range of a histogram adjustment display to include a sensible range
    of values.
    """
    start: float
    end: float
    min: float
    max: float


class DisplaySettings(Base):
    """
    Metadata for display settings.
    """

    contrast_limits: ContrastLimits
    color: Optional[Color]
    invert_lut: bool


class DataSource(Base):
    """
    A representation of some describable, accessible piece of
    spatial data.
    """
    name: str
    description: str
    url: str
    format: str
    transform: SpatialTransform


class Mesh(DataSource):
    """
    A mesh, parametrized by a format and a list of integer ids
    """
    format: MeshFormat
    ids: List[int]


class MeshRead(Mesh):
    id: int


class MeshCreate(Mesh):
    pass


class MeshUpdate(Mesh):
    pass


class Image(DataSource):
    format: ArrayContainerFormat
    sampleType: SampleType
    contentType: ContentType
    displaySettings: DisplaySettings
    subsources: List[Mesh]


class ImageRead(Image):
    id: int


class ImageCreate(Image):
    pass


class ImageUpdate(Image):
    pass
