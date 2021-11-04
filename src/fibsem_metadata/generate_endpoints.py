# update index.json
from fibsem_metadata.utils import materialize_element
import click
from pathlib import Path
from fibsem_metadata.models.manifest import DatasetManifest
from fibsem_metadata.models.metadata import DatasetMetadata
from fibsem_metadata.models.views import DatasetViews
from fibsem_metadata.models.sources import VolumeSource

def validate_tree(root: str):
    """
    root must be a string naming a directory tree that contains a
    directory called "datasets" populated with directories with variable
    names, which contain a subdirectory called "sources"
    """
    datasets_path = (Path(root) / 'metadata')
    if not (datasets_path.exists() and datasets_path.is_dir()):
        raise OSError(f'Metadata directory {str(datasets_path)} is invalid.')

    for subpath in datasets_path.glob('*'):
        manifest_file = subpath / 'manifest.json'
        if not (manifest_file.exists() and manifest_file.is_file()):
            raise FileNotFoundError(f'Could not find {str(manifest_file)}')


def build_manifest(dataset_path: str):
    root = Path(dataset_path)
    manifest_path = root / 'manifest.json'
    source_paths = (root / 'sources').glob('*.json')
    metadata_path = root / 'metadata.json'
    views_path = root / 'views.json'
    name = root.parts[-1]

    volumes = [materialize_element(path, VolumeSource) for path in source_paths]
    views = materialize_element(views_path, DatasetViews)
    metadata = materialize_element(metadata_path, DatasetMetadata)
    manifest = DatasetManifest(name=name,
                               metadata=metadata,
                               volumes=volumes,
                               views=views.views)
    manifest_path.write_text(manifest.json(indent=2))
    return 1


@click.command()
@click.argument('root', type=click.Path(exists=True, file_okay=False))
def main(root: str):
    paths = filter(lambda v: v.is_dir(), Path(root).glob('*'))
    return [build_manifest(path) for path in paths]


if __name__ == "__main__":
    main()
