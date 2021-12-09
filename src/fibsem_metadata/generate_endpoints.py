from typing import Union
from fibsem_metadata.models.index import Index
from fibsem_metadata.utils import materialize_element
import click
from pathlib import Path
from fibsem_metadata.models.manifest import DatasetManifest
from fibsem_metadata.models.metadata import DatasetMetadata
from fibsem_metadata.models.views import DatasetViews
from fibsem_metadata.models.sources import VolumeSource
from shutil import copyfile

def validate_tree(root: str) -> None:
    """
    root must be a string naming a directory tree that contains a
    directory called "datasets" populated with directories with variable
    names, which contain a subdirectory called "sources"
    """
    datasets_path = Path(root) / "metadata"
    if not (datasets_path.exists() and datasets_path.is_dir()):
        raise OSError(f"Metadata directory {str(datasets_path)} is invalid.")

    for subpath in datasets_path.glob("*"):
        manifest_file = subpath / "manifest.json"
        if not (manifest_file.exists() and manifest_file.is_file()):
            raise FileNotFoundError(f"Could not find {str(manifest_file)}")


def build_manifest(dataset_path: Union[Path, str], output_dir: Union[Path, str]) -> int:
    root = Path(dataset_path)
    name = root.parts[-1]
    manifest_path = output_dir / "manifest.json"
    source_paths = (root / "sources").glob("*.json")
    metadata_path = root / "metadata.json"
    views_path = root / "views.json"
    thumbnail_path = root / "thumbnail.jpg"

    volumes = [materialize_element(path, VolumeSource) for path in source_paths]
    views = materialize_element(views_path, DatasetViews)
    metadata = materialize_element(metadata_path, DatasetMetadata)
    manifest = DatasetManifest(
        name=name, metadata=metadata, volumes=volumes, views=views.views
    )
    
    if not output_dir.exists():
        output_dir.mkdir()
    # write manifest and thumbnail to API destination
    manifest_path.write_text(manifest.json(indent=2))
    copyfile(thumbnail_path, output_dir / thumbnail_path.name)
    return 0


@click.command()
@click.argument("root", type=click.Path(exists=True, file_okay=False))
def main(root: str='.') -> int:
    metadata_paths = tuple(filter(lambda v: v.is_dir(), Path(root).glob("metadata/*")))
    # prepare default output
    api_dir = Path("api")
    if not api_dir.exists():
        api_dir.mkdir()
    # generate the manifest
    api_paths = [api_dir / path.name for path in metadata_paths]
    [build_manifest(meta_source, meta_target) for meta_source, meta_target in zip(metadata_paths, api_paths)]
    # generate the index
    index = Index(datasets=tuple(map(str, metadata_paths)))
    with open(Path(root) / "api/index.json", mode="w") as fh:
        fh.write(index.json())
    return 0


if __name__ == "__main__":
    main()
