# update index.json
import json
import click
from pathlib import Path
from fibsem_metadata.index import DatasetIndex
from fibsem_metadata.index import DatasetIndex, VolumeSource, DatasetViewCollection
from typing import Union, Any, Dict


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


def main(index_path: str, element_path: str):
    old_index = DatasetIndex.parse_file(index_path)

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
@click.argument("index_path", type=click.Path(exists=True, dir_okay=False))
@click.argument("element_path", type=click.Path(exists=True, dir_okay=True))
def main_cli(index_path: str, element_path: str):
    return main(index_path, element_path)


if __name__ == "__main__":
    main_cli()
