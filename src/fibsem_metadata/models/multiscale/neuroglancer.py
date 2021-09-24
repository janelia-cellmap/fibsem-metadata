from pydantic import BaseModel, PositiveInt
from typing import Sequence
import click


class PixelResolution(BaseModel):
    """
    PixelResolution attribute used by the saalfeld lab. The dimensions attribute contains a list of scales that define the
    grid spacing of the data, in F-order.
    """

    dimensions: Sequence[float]
    unit: str


# todo: validate argument lengths
class NeuroglancerN5GroupMetadata(BaseModel):
    """
    Metadata to enable displaying an N5 group containing several datasets as a multiresolution dataset in neuroglancer.
    see https://github.com/google/neuroglancer/issues/176#issuecomment-553027775
    Axis properties will be indexed in the opposite order of C-contiguous axis indexing.
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
