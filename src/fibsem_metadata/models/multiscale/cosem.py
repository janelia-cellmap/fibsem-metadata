from pydantic import root_validator
from pydantic import validator
from sqlmodel import SQLModel
from typing import Literal, Any


class ScaleTranslate(SQLModel):
    units: list[Any]
    translate: list[Any]
    scale: list[Any]

    @root_validator
    def validate_argument_length(
        cls: "ScaleTranslate", values: dict[str, list[str] | list[float]]]
    ) -> dict[str, list[str] | list[float]]:
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
    units: list[Literal['indices']]
    translate: list[int]
    scale: list[Literal[1]]

    @validator('axes')
    def axes_must_be_stringed_ints(cls, v: list[str]):
        for idx, element in enumerate(v):
            if element != str(idx):
                raise ValueError(f'Invalid axis name. Got {element}, expected "{str(idx)}"')



class SpatialTransform(ScaleTranslate):
    """
    Representation of an N-dimensional scaling + translation transform for labelled axes with units.
    """

    axes: list[str]
    units: list[str]
    translate: list[float]
    scale: list[float]


class ScaleMeta(SQLModel):
    path: str
    transform: SpatialTransform


class MultiscaleMeta(SQLModel):
    datasets: list[ScaleMeta]


class COSEMGroupMetadata(SQLModel):
    """
    Multiscale metadata used by COSEM for multiscale datasets saved in N5/Zarr groups.
    """

    name: str
    multiscales: list[MultiscaleMeta]