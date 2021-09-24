from enum import Enum
from click.decorators import group
from pydantic import BaseModel
from typing import Sequence, Optional, Union
from pydantic.color import Color
from fibsem_metadata.models.multiscale.cosem import SpatialTransform
import fsspec
import json
import click
  
class MultiscaleN5Validity(BaseModel):
    group_meta_exists: bool = False


def validate_multiscale_n5(path: str, dataType: str) -> MultiscaleN5Validity:
    """
    Check that an n5-backed volume located at `path` has the following 
    properties:
    - `path/attributes.json` exists
    - `path/attributes.json` contains valid multiscale metadata 
    - The datasets enumerated in the `datasets` property of the multiscale 
    metadata exist, and each have valid metadata.
    - The datatype of all the volumes matches `dataType`
    """
    mapper = fsspec.get_mapper(path)
    validity = MultiscaleN5Validity()
    group_meta_bytes: Union[None, bytes] = mapper.get('attributes.json')
    if group_meta_bytes is not None:
        group_meta = json.loads(group_meta_bytes)
        validity.group_meta_exists = True

    return validity


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


class ContrastLimits(BaseModel):
    """
    Metadata for contrast limits. Currently these values are in normalized units, i.e. drawn from the interval [0,1]
    """

    start: float = 0.0
    end: float = 1.0
    min: float = 0.0
    max: float = 1.0


class DisplaySettings(BaseModel):
    """
    Metadata for display settings
    """

    contrastLimits: ContrastLimits = ContrastLimits()
    color: Color = "white"
    invertLUT: bool = False


class DataSource(BaseModel):
    name: str
    path: str
    format: str
    transform: SpatialTransform
    description: str = ""
    version: str = "0"
    tags: Sequence[str] = []


class MeshSource(DataSource):
    format: MeshTypeEnum
    ids: Sequence[int]


class VolumeSource(DataSource):
    format: ArrayContainerTypeEnum
    dataType: str
    contentType: ContentTypeEnum
    displaySettings: DisplaySettings

    subsources: Sequence[MeshSource] = []


class DatasetView(BaseModel):
    name: str
    description: str
    position: Optional[Sequence[float]]
    scale: Optional[float]
    orientation: Optional[Sequence[float]]
    volumeNames: Sequence[str]


class DatasetViewCollection(BaseModel):
    views: Sequence[DatasetView]


class DatasetIndex(BaseModel):
    name: str
    volumes: Sequence[VolumeSource]
    views: Sequence[DatasetView]


@click.command()
def main() -> None:
    print(DatasetIndex.schema_json(indent=2))


if __name__ == "__main__":
    main()
