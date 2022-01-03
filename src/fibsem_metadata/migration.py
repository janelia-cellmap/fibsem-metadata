import json
from typing import Any, Dict
import click
from glob import glob

from fibsem_metadata.models.sources import VolumeSource
from fibsem_metadata.models.views import DatasetViews
from pydantic import ValidationError


def is_view(path: str) -> bool:
    if path.endswith('views.json'):
        return True
    else:
        return False


def migrate_source(blob: Dict[str, Any]) -> VolumeSource:
    try:
        return VolumeSource(**blob)
    except ValidationError:
        uri = blob.pop("URI")
        blob['url'] = uri
        return VolumeSource(**blob)


def migrate_views(blob: Dict[str, Any]) -> DatasetViews:
    try:
        return DatasetViews(**blob)
    except ValidationError:
        for element in blob["views"]:
            sources = element.pop("volumeNames")
            element["sources"] = sources
        return DatasetViews(**blob)


def migrate_element(path: str) -> int:
    with open(path) as fh:
        blob = json.load(fh)

    if is_view(path):
        migrated = migrate_views(blob)
    else:
        migrated = migrate_source(blob)

    write_blob = migrated.json(indent=2)
    with open(path, mode="w") as fh:
        fh.write(write_blob)

    return 0


@click.command()
@click.argument("paths", type=click.Path(exists=True, dir_okay=False), nargs=-1)
def migrate(paths: str) -> int:
    _ = [migrate_element(path) for path in paths]
    return 0


if __name__ == "__main__":
    migrate()
