from pydantic import PositiveInt
from ..base import StrictBaseModel
from typing import Sequence
import click


class PixelResolution(StrictBaseModel):
    """
    PixelResolution attribute used by the saalfeld lab.
    The dimensions attribute contains a list of scales that define the
    grid spacing of the data, in F-order.
    """

    dimensions: Sequence[float]
    unit: str


# todo: validate argument lengths
class NeuroglancerN5GroupMetadata(StrictBaseModel):
    """
    Metadata to enable displaying an N5 group containing several datasets
    as a multiresolution dataset in neuroglancer. See
    https://github.com/google/neuroglancer/issues/176#issuecomment-553027775
    Axis properties are in F-order.
    """

    axes: Sequence[str]
    units: Sequence[str]
    scales: Sequence[Sequence[PositiveInt]]
    pixelResolution: PixelResolution


@click.command()
def main() -> None:
    print(NeuroglancerN5GroupMetadata.schema_json(indent=2))


if __name__ == "__main__":
    main()
