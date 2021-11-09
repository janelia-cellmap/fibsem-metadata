import pytest
from glob import glob
import json
import fsspec
from typing import Any, Dict
from fibsem_metadata.models.views import DatasetViews
from fibsem_metadata.models.sources import VolumeSource

volume_sources = glob('metadata/*/sources/*')
views = glob('metadata/*/views.json')

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
    assert exists_fsspec(vsource.URI)

    for subsource in vsource.subsources:
        assert exists_fsspec(subsource.URI)

@pytest.mark.parametrize('views_path', views)
def test_view(views_path):
    blob = get_json_blob(views_path)
    views = DatasetViews(**blob)        
