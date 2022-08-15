from typing import Dict, Sequence

import click

from fibsem_metadata.legacy_models.base import StrictBaseModel
from fibsem_metadata.legacy_models.metadata import DatasetMetadata
from fibsem_metadata.legacy_models.sources import VolumeSource
from fibsem_metadata.legacy_models.views import DatasetView


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
