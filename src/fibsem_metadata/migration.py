import json
from typing import Any, Dict
import click
from glob import glob


def migrate_source(path: str) -> int:
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

    return 0


@click.command()
@click.argument("paths", type=click.Path(exists=True, dir_okay=False), nargs=-1)
def migrate(paths: str) -> int:
    x = [migrate_source(path) for path in paths]
    return 0


if __name__ == "__main__":
    migrate()
