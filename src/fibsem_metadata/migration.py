import json
from typing import Any, Dict
import click
from glob import glob


def migrate_source(path: str) -> None:
    with open(path) as fh:
        blob = json.load(fh)
    try:
        blob["URI"] = blob.pop("path")
        subsources = []
        for subsource in blob["subsources"]:
            subsource["URI"] = subsource.pop("path")
            subsources.append(subsource)
        blob["subsources"] = subsources
    except KeyError:
        pass
    with open(path, mode="w") as fh:
        json.dump(blob, fh, indent=2)

    return None


@click.command()
@click.argument("paths", type=click.Path(exists=True, dir_okay=False), nargs=-1)
def migrate(paths: str):
    [migrate_source(path) for path in paths]


if __name__ == "__main__":
    migrate()
