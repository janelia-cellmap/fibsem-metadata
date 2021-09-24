from pydantic import BaseModel, root_validator
from typing import Sequence, Union, Dict, List
import click


class SpatialTransform(BaseModel):
    """
    Representation of an N-dimensional scaling + translation transform for labelled axes with units.
    """

    axes: Sequence[str]
    units: Sequence[str]
    translate: Sequence[float]
    scale: Sequence[float]

    @root_validator
    def validate_argument_length(
        cls, values: Dict[str, Union[Sequence[str], Sequence[float]]]
    ):
        scale = values.get("scale")
        axes = values.get("axes")
        units = values.get("units")
        translate = values.get("translate")
        if not len(axes) == len(units) == len(translate) == len(scale):
            raise ValueError(
                f"The length of all arguments must match. {len(axes) = },  {len(units) = }, {len(translate) = }, {len(scale) = }"
            )
        return values


class ScaleMeta(BaseModel):
    path: str
    transform: SpatialTransform


class MultiscaleMeta(BaseModel):
    datasets: Sequence[ScaleMeta]


class COSEMGroupMetadata(BaseModel):
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
