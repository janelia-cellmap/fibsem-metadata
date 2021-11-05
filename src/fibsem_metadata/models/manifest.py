import click
from typing import Sequence
from fibsem_metadata.models.metadata import DatasetMetadata
from fibsem_metadata.models.sources import VolumeSource
from fibsem_metadata.models.views import DatasetView
from pydantic import BaseModel


class DatasetManifest(BaseModel):
    name: str
    metadata: DatasetMetadata
    volumes: Sequence[VolumeSource]
    views: Sequence[DatasetView]


@click.command()
def main() -> None:
    click.echo(DatasetManifest.schema_json(indent=2))


if __name__ == "__main__":
    main()
