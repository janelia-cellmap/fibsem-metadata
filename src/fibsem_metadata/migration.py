import json
from typing import Any, Dict
import click

from fibsem_metadata.models.sources import VolumeSource
from fibsem_metadata.models.views import DatasetViews
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def is_view(path: str) -> bool:
    if path.endswith('views.json'):
        return True
    else:
        return False


def clean_datasource(blob: Dict[str, Any]) -> Dict[str, Any]:
    remap = {"tags": None,
             "version": None,
             "dataType": None,
             "URI": "url",
             "path": "url"}
    for key, value in remap.items():
        if key in blob:
            if value is not None:
                blob[value] = blob.pop(key)
            else:
                blob.pop(key)
    return blob


def migrate_source(blob: Dict[str, Any]) -> VolumeSource:
    try:
        return VolumeSource(**blob)
    except ValidationError:
        blob = clean_datasource(blob)
        if "subsources" in blob:
            for idx, mesh in enumerate(blob["subsources"]):
                blob["subsources"][idx] = clean_datasource(mesh)

        return VolumeSource(**blob)


def migrate_views(blob: Dict[str, Any]) -> DatasetViews:
    try:
        return DatasetViews(**blob)
    except ValidationError:
        for element in blob["views"]:
            if "volumeNames" in element:
                element["sources"] = element.pop("volumeNames")
        return DatasetViews(**blob)


def migrate_element(path: str) -> int:
    logger.info(f"Preparing {path}")
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
