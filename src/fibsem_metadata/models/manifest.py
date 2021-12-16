import click
from typing import Sequence, Dict, Union
from fibsem_metadata.models.base import StrictBaseModel
from fibsem_metadata.models.metadata import DatasetMetadata
from fibsem_metadata.models.sources import MeshSource, VolumeSource
from fibsem_metadata.models.views import DatasetView


class DatasetManifest(StrictBaseModel):
    name: str
    metadata: DatasetMetadata
    sources: Dict[str, VolumeSource]
    views: Sequence[DatasetView]


@click.command()
def main() -> None:
    click.echo(DatasetManifest.schema_json(indent=2))


if __name__ == "__main__":
    main()
