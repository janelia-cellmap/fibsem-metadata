from fibsem_metadata.models.dataset import Dataset
from pydantic import ValidationError
import click
import json

def validate_readme(path):
    with open(path, mode='r') as fh:
        try:
            Dataset(**json.load(fh))
            return 0
        except ValidationError as e:
            return e

@click.command()
@click.argument('paths', type=click.Path(exists=True), nargs=-1)
def main(paths):
    results = {path: validate_readme(path) for path in paths} 
    click.echo(results)
        
if __name__ == '__main__':
    main()    