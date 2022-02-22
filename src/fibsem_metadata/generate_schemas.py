from os import remove
import logging
import click
from pathlib import Path
from fibsem_metadata.models.manifest import DatasetManifest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@click.command()
@click.argument("root", type=click.Path(exists=True, file_okay=False))
def main(root: str = ".") -> int:
    schema_dir = Path("schemas")
    if not schema_dir.exists():
        schema_dir.mkdir()
    else:
        for child in schema_dir.glob("*"):
            if child.is_dir():
                rmtree(child)
            else:
                remove(child)
    # generate the schemas

    with open(Path(root) / schema_dir / "manifest.schema.json", mode="w") as fh:
        fh.write(DatasetManifest.schema_json(indent=2))
    return 0


if __name__ == "__main__":
    main()
