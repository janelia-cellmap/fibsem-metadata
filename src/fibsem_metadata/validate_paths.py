import fsspec
import click
from pathlib import Path
import json
from pydantic import BaseModel
from typing import Union
from pathlib import Path

class MultiscaleN5Validity(BaseModel):
    group_meta_exists: bool = False

def validate_path(path: str):
    fs = fsspec.get_mapper(path).fs
    return fs.exists(path)

def validate_multiscale_n5(path: str) -> MultiscaleN5Validity:
    """
    Check that an n5-backed volume located at `path` has the following 
    properties:
    - `path/attributes.json` exists
    - `path/attributes.json` contains valid multiscale metadata 
    - The datasets enumerated in the `datasets` property of the multiscale 
    metadata exist, and each have valid metadata.
    - The datatype of all the volumes matches `dataType`
    """
    mapper = fsspec.get_mapper(path)
    validity = MultiscaleN5Validity()
    group_meta_bytes: Union[None, bytes] = mapper.get('attributes.json')
    if group_meta_bytes is not None:
        group_meta = json.loads(group_meta_bytes)
        validity.group_meta_exists = True

    return validity


@click.command()
@click.argument('source_paths', type=click.Path(exists=True, dir_okay=False), nargs=-1)
def main(source_paths: str):
    result = {}
    for path in source_paths:
        source = json.loads(Path(path).read_text())
        dataset = Path(path).parent.parent.name
        if dataset not in result:
            result[dataset] = []
        result[dataset].append({'name' : source['name'], 'validate_multiscale_n5' : validate_multiscale_n5(source['path']).dict() })
    result_json = json.dumps(result, indent=2)
    click.echo(result_json)

if __name__ == '__main__':
    main()