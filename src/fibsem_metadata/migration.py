import json
from typing import Any, Dict
import click
from glob import glob
from fibsem_metadata.models.sources import VolumeSource
from pydantic import ValidationError

def migrate_source(path: str) -> int:
    with open(path) as fh:
        blob = json.load(fh)
    try:
        blob["url"] = blob.pop("URI")
        subsources = []
        for subsource in blob["subsources"]:
            subsource["url"] = subsource.pop("URI")
            subsources.append(subsource)
        blob["subsources"] = subsources
    except KeyError:
        pass
    for extra_key in ("dataType", "tags", "version"):
        if extra_key in blob:
            blob.pop(extra_key)
        for subsource in blob["subsources"]:
            if extra_key in subsource:
                subsource.pop(extra_key)
    # validate
    try:
        v = VolumeSource(**blob)
    except ValidationError as e:
        raise e
    with open(path, mode="w") as fh:
        json.dump(blob, fh, indent=2)

    return 0


@click.command()
@click.argument("paths", type=click.Path(exists=True, dir_okay=False), nargs=-1)
def migrate(paths: str) -> int:
    x = [migrate_source(path) for path in paths]
    return 0


if __name__ == "__main__":
    migrate()
