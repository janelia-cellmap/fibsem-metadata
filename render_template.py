from pathlib import Path
from jinja2 import Template, Environment
import json
import click


def render_template(template_path: str, metadata_path: str):
    readme_metadata = json.loads(Path(metadata_path).read_text())
    template = Template(Path(template_path).read_text())
    return template.render(fields=readme_metadata)

@click.command()
@click.argument('template')
@click.argument('metadata')
@click.argument('output')
def main(template, metadata, output):
    rendered = render_template(template, metadata)
    Path(output).write_text(rendered)

if __name__ == '__main__':
    main()
        

