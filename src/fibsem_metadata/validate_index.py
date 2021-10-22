from fibsem_metadata.models.index import DatasetIndex
from pydantic import ValidationError
import click
import json

def validate(path, cls):
    with open(path, mode='r') as fh:
        try:
            cls(**json.load(fh))
            return 0
        except ValidationError as e:
            return e

@click.command()
@click.argument('paths', type=click.Path(exists=True), nargs=-1)
def main(paths):
    results = {path: validate(path, DatasetIndex) for path in paths} 
    click.echo(results)
        
if __name__ == '__main__':
    main()    