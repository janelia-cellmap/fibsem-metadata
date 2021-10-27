import json
from fibsem_metadata.models.index import ContrastLimits
from pydantic import ValidationError
import click
from typing import List


def denormalize_contrast_limits(element_path: str):
    with open(element_path) as fh:
        blob = json.load(fh)
    old_clims = blob["displaySettings"]["contrastLimits"]
    if old_clims["max"] > 1.0:
        new_display = ContrastLimits(**old_clims)
        click.echo(f"{element_path} is fine")
    else:
        click.echo(f"{element_path} gets changed")
        dtype = blob["dataType"]
        if dtype == "uint8":
            maxval = 255
        elif dtype == "uint16":
            maxval = 65535
        elif dtype == "uint32":
            maxval = 4294967295
        elif dtype == "uint64":
            maxval = 1
        new_display = ContrastLimits(
            start=int(old_clims["start"] * maxval),
            end=int(old_clims["end"] * maxval),
            min=int(old_clims["min"] * maxval),
            max=int(old_clims["max"] * maxval),
        )

    blob["displaySettings"]["contrastLimits"] = new_display.dict()
    with open(element_path, mode="w") as fh:
        json.dump(blob, fh, indent=2)
    return None


@click.command()
@click.argument("paths", type=click.Path(exists=True), nargs=-1)
def main(paths: List[str]):
    return [denormalize_contrast_limits(p) for p in paths]


if __name__ == "__main__":
    main()
