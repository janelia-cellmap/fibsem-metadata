import pytest
from glob import glob
import json
import fsspec
from typing import Any, Dict
from fibsem_metadata.models.index import DatasetViewCollection, VolumeSource, DatasetView

volume_sources = glob('metadata/datasets/*/sources/*')
views = glob('metadata/datasets/*/views.json')


def exists_fsspec(path: str) -> bool:
    return fsspec.get_mapper(path).fs.exists(path)


def get_json_blob(path: str) -> Dict[str, Any]:
    with open(path, mode='r') as fh:
        blob = json.load(fh)
    return blob


@pytest.mark.parametrize('path', volume_sources)
def test_volume_source(path: str):
    blob = get_json_blob(path)
    vsource = VolumeSource(**blob)
    assert exists_fsspec(path)

    for subsource in vsource.subsources:
        assert exists_fsspec(subsource.path)

@pytest.mark.parametrize('path', views)
def test_view(path: str):
    blob = get_json_blob(path)
    view = DatasetViewCollection(**blob)
