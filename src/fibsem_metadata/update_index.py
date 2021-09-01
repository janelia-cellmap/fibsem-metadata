# update index.json
import json
import click
from fibsem_metadata.index import DatasetIndex
from fibsem_metadata.index import DatasetIndex, VolumeSource, DatasetViewCollection
from typing import Union, Any, Dict

def materialize_element(json_blob: Dict[str, Any]) -> Union[VolumeSource, DatasetViewCollection]:
    if 'views' in json_blob:
        return DatasetViewCollection(**json_blob)
    else:
        return VolumeSource(**json_blob)


def main(index_path: str, element_path: str):
    old_index = DatasetIndex.parse_file(index_path)
    new_index = old_index.copy()
    with open(element_path, 'r') as fh:
        new_element: Union[VolumeSource, DatasetViewCollection] = materialize_element(json.load(fh))

    if isinstance(new_element, VolumeSource):
        new_volumes = list(new_index.volumes)
        for idx, volume in enumerate(new_volumes):
            if volume.name == new_element.name:
                new_volumes[idx] = new_element
        new_index.volumes = new_volumes
    else:
        new_index.views = new_element.views

    with open(index_path, mode='w') as fh:
        fh.write(new_index.json(indent=2))
    return 1

@click.command()
@click.argument('index_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('element_path', type=click.Path(exists=True, dir_okay=False))
def main_cli(index_path: str, element_path: str):
    return main(index_path, element_path)

if __name__ == '__main__':
    main_cli()
