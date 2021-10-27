# update index.json
import json
import click
import os
from pathlib import Path
from fibsem_metadata.models.index import DatasetIndex
from fibsem_metadata.models.index import DatasetIndex, VolumeSource, DatasetViewCollection
from typing import Union, Any, Dict


def find_index(element_path: str) -> str:
    return os.path.join(*element_path.rstrip(os.path.sep).split(os.path.sep)[:-1], 'index.json') 


def materialize_element(path: str) -> Union[VolumeSource, DatasetViewCollection]:
    with open(path, mode="r") as fh:
        json_blob = json.load(fh)
        if "views" in json_blob:
            return DatasetViewCollection(**json_blob)
        else:
            return VolumeSource(**json_blob)


def append_element(
    index: DatasetIndex, new_element: Union[VolumeSource, DatasetViewCollection]
) -> DatasetIndex:
    new_index = index.dict()
    if isinstance(new_element, VolumeSource):
        new_volumes = new_index["volumes"]
        for idx, volume in enumerate(new_volumes):
            if volume['name'] == new_element.name:
                new_volumes[idx] = new_element
        new_index["volumes"] = new_volumes
    else:
        new_index["views"] = new_element.views
    return DatasetIndex(**new_index)


def sync_elements(index: DatasetIndex, element_path: str) -> DatasetIndex:
    new_index = index.dict()
    new_index["volumes"] = sorted(
        list(map(materialize_element, Path(element_path).glob("*.json"))),
        key=lambda v: v.name,
    )
    return DatasetIndex(**new_index)


def update_index(element_path: str):
    index_path = find_index(element_path)
    name = index_path.split(os.path.sep)[-2]
    if os.path.exists(index_path):
        old_index = DatasetIndex.parse_file(index_path)
    else:
        old_index = DatasetIndex(name=name, volumes=[], views=[])

    # syncing
    if Path(element_path).is_dir():
        new_index = sync_elements(old_index, element_path)

    # appending
    else:
        new_element: Union[VolumeSource, DatasetViewCollection] = materialize_element(
            element_path
        )
        new_index = append_element(old_index, new_element)

    with open(index_path, mode="w") as fh:
        fh.write(new_index.json(indent=2))
    return 1


@click.command()
@click.argument("paths", type=click.Path(exists=True, dir_okay=True), nargs=-1)
def main(paths: str):
    return [update_index(path) for path in paths]


if __name__ == "__main__":
    main()
