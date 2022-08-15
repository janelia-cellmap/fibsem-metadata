from typing import Dict, List, Sequence, Union

import click
from pydantic import root_validator

from ..base import StrictBaseModel


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
