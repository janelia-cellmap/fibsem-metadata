from typing import List, Union, Dict
from pydantic import root_validator
from pydantic import validator
from typing import Literal, Any
from ..base import Base


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
