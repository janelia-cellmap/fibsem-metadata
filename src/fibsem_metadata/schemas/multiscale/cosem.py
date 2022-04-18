from pydantic import root_validator
from pydantic import validator
from ..base import StrictBaseModel
from typing import List, Sequence, Union, Dict, Literal
import click


class SpatialTransform(StrictBaseModel):
    """
    Representation of an N-dimensional scaling + translation transform for labelled axes with units.
    """

    axes: Sequence[str]
    units: Sequence[str]
    translate: Sequence[float]
    scale: Sequence[float]

    @root_validator
    def validate_argument_length(
        cls: "SpatialTransform", values: Dict[str, Union[List[str], List[float]]]
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


class OffsetTransform(SpatialTransform):
    """
    A transform representing the intrinsic array-indexing-based space of
    N-dimensional arrays. For each axis, the axis name must be a the string
    representation of an integer starting from 0, the unit must be 'indices',
    the scale must be 1, and the offset must be an integer.
    """
    units: Sequence[Literal['indices']]
    translate: Sequence[int]
    scale: Sequence[Literal[1]]

    @validator('axes')
    def axes_must_be_stringed_ints(cls, v: Sequence[str]):
        for idx, element in enumerate(v):
            if element != str(idx):
                raise ValueError(f'Invalid axis name. Got {element}, expected "{str(idx)}"')


class ScaleMeta(StrictBaseModel):
    path: str
    transform: SpatialTransform


class MultiscaleMeta(StrictBaseModel):
    datasets: Sequence[ScaleMeta]


class COSEMGroupMetadata(StrictBaseModel):
    """
    Multiscale metadata used by COSEM for multiscale datasets saved in N5/Zarr groups.
    """

    name: str
    multiscales: Sequence[MultiscaleMeta]


@click.command()
def main() -> None:
    print(COSEMGroupMetadata.schema_json(indent=2))


if __name__ == "__main__":
    main()
