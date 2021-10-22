import pytest
from glob import glob
import json
import fsspec

from fibsem_metadata.models.index import VolumeSource

volume_sources = glob('metadata/datasets/*/sources/*')


def exists_fsspec(path: str) -> bool:
    return fsspec.get_mapper(path).fs.exists(path)


@pytest.mark.parametrize('path', volume_sources)
def test_volume_source(path: str):
    with open(path, mode='r') as fh:
        blob = json.load(fh)
    vsource = VolumeSource(**blob)
    assert exists_fsspec(path)

    for subsource in vsource.subsources:
        assert exists_fsspec(subsource.path)
