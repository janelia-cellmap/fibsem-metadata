import json
from typing import Any, Dict
import click
from pydantic import HttpUrl

from fibsem_metadata.models.sources import VolumeSource
from fibsem_metadata.models.metadata import Hyperlink, DatasetMetadata
from fibsem_metadata.models.views import DatasetViews
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


pub_mapping = {'Xu et al., 2020' : Hyperlink(href=HttpUrl('https://doi.org/10.1038/s41586-021-03992-4', scheme='https', host='doi.org'), title='Xu et al., 2021'),
            'Heinrich et al., 2020' : Hyperlink(href=HttpUrl('https://doi.org/10.1038/s41586-021-03977-3', scheme='https', host='doi.org'), title='Heinrich et al., 2021'),
            'Weigel, Chang, et al., 2021' : Hyperlink(href=HttpUrl('https://doi.org/10.1016/j.cell.2021.03.035', scheme='https', host='doi.org'), title='Weigel, Chang, et al., 2021'),
            'Ritter et al., 2021' : Hyperlink(href=HttpUrl('about:blank', scheme='https', host='doi.org'), title='Ritter et al., 2022'),
            'Mueller et al., 2020' : Hyperlink(href=HttpUrl('https://doi.org/10.1083/jcb.202010039', scheme='https', host='doi.org'), title='Mueller et al., 2020'),
            'Hoffman et al., 2020' : Hyperlink(href=HttpUrl('https://doi.org/10.1126/science.aaz5357', scheme='https', host='doi.org'), title='Hoffman et al., 2020'),
            'Coulter et al., 2018' : Hyperlink(href=HttpUrl('https://doi.org/10.1016/j.celrep.2018.06.100', scheme='https', host='doi.org'), title='Coulter et al., 2018')}

def categorize_file(path: str) -> str:
    if path.endswith('views.json'):
        result = 'views'
    elif path.endswith('metadata.json'):
        result = 'metadata'
    else:
        result = 'source'
    return result


def clean_datasource(blob: Dict[str, Any]) -> Dict[str, Any]:
    return blob


def migrate_source(blob: Dict[str, Any]) -> VolumeSource:
    try:
        return VolumeSource(**blob)
    except ValidationError:
        blob = clean_datasource(blob)
        if "subsources" in blob:
            for idx, mesh in enumerate(blob["subsources"]):
                blob["subsources"][idx] = clean_datasource(mesh)

        return VolumeSource(**blob)

def migrate_metadata(blob: Dict[str, Any]) -> DatasetMetadata:
    publications = blob.pop('publications')
    new_pubs = []
    for pub in publications:
        if pub in pub_mapping:
            new_pub = pub_mapping[pub]
            new_pubs.append(new_pub)
        else:
            new_pubs.append(pub)
    blob['publications'] = new_pubs
    return DatasetMetadata(**blob)

def migrate_views(blob: Dict[str, Any]) -> DatasetViews:
    try:
        return DatasetViews(**blob)
    except ValidationError:
        for element in blob["views"]:
            if "volumeNames" in element:
                element["sources"] = element.pop("volumeNames")
        return DatasetViews(**blob)


def migrate_element(path: str) -> int:
    logger.info(f"Preparing {path}")
    typ = categorize_file(path)
    with open(path) as fh:
        blob = json.load(fh)
    if typ == 'views':
        migrated = migrate_views(blob)
    elif typ == 'metadata':
        migrated = migrate_metadata(blob)
    else:
        migrated = migrate_source(blob)

    write_blob = migrated.json(indent=2)
    with open(path, mode="w") as fh:
        fh.write(write_blob)

    return 0


@click.command()
@click.argument("paths", type=click.Path(exists=True, dir_okay=False), nargs=-1)
def migrate(paths: str) -> int:
    _ = [migrate_element(path) for path in paths]
    return 0


if __name__ == "__main__":
    migrate()
