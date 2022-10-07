import base64
from glob import glob
import requests
from typing import Dict, List, Literal, Optional
import json
from sqlalchemy.orm import Session
from rich import print_json

from fibsem_metadata.db.session import SessionLocal, engine
from fibsem_metadata.legacy_models.manifest import DatasetManifest
from fibsem_metadata.legacy_models.metadata import (
    DatasetMetadata as LegacyDatasetMetadata,
)
from fibsem_metadata.legacy_models.metadata import DatasetView as LegacyView
from fibsem_metadata.legacy_models.metadata import (
    FIBSEMImagingMetadata as LegacyFIBSEMAcquisition,
)
from fibsem_metadata.legacy_models.metadata import Publication as LegacyPublication
from fibsem_metadata.legacy_models.metadata import SampleMetadata as LegacySample
from fibsem_metadata.models.acquisition import UnitfulVector
from fibsem_metadata.models.source import ContrastLimits, DisplaySettings, Image
from fibsem_metadata.schemas import (
    DatasetTable,
    FIBSEMAcquisitionTable,
    PublicationTable,
    SampleTable,
    ViewTable,
    ImageTable,
)
from typing import List, Dict, Any


def fetch_json() -> List[Dict[str, Any]]:
    branch = "stable"
    url = "https://api.github.com/repos/janelia-cosem/fibsem-metadata/contents/api"
    headers = {"Accept": "application/vnd.github+json"}
    request = requests.get(f"{url}?={branch}", headers=headers)
    if request.status_code != 200:
        raise RuntimeError(
            f"The status code is bad! it was {request.status_code} instead of 200!!!!!!"
        )
    api_contents = request.json()
    blobs = []
    for entry in api_contents:
        name = entry["name"]
        if name != "index.json":
            payload = requests.get(
                f"{url}/{name}/manifest.json?={branch}", headers=headers
            ).json()
            blob = json.loads(base64.b64decode(payload["content"]))
            blobs.append(blob)

    return blobs


def get_json() -> List[Dict[str, Any]]:
    files = glob("./api/*/manifest.json")
    blobs = []
    for file in files:
        with open(file, mode="r") as fh:
            blobs.append(json.load(fh))

    return blobs


def legacy_create_sample(metadata: LegacySample) -> SampleTable:
    sample = SampleTable(
        organism=metadata.organism,
        type=metadata.type,
        subtype=metadata.subtype,
        treatment=metadata.treatment,
        contributions=metadata.contributions,
        protocol=metadata.protocol,
        description=metadata.description,
    )
    return sample


def legacy_create_acquisition(
    metadata: LegacyFIBSEMAcquisition,
    instrument: str = "",
    grid_shape: Dict[str, int] = {"z": 0, "z": 0, "x": 0},
    grid_unit: str = "nm",
) -> FIBSEMAcquisitionTable:

    acq = FIBSEMAcquisitionTable(
        name="",
        instrument=instrument,
        institution=metadata.institution,
        start_date=metadata.startDate,
        grid_spacing=metadata.gridSpacing.dict(),
        dimensions=UnitfulVector(unit=grid_unit, values=grid_shape).dict(),
        bias_voltage=metadata.biasVoltage,
        scan_rate=metadata.scanRate,
        current=metadata.current,
        primary_energy=metadata.primaryEnergy,
    )

    return acq


def legacy_create_pub(
    metadata: LegacyPublication, type: Literal["DOI", "publication"]
) -> PublicationTable:

    pub = PublicationTable(name=metadata.title, url=metadata.href, type=type.lower())
    return pub


def legacy_create_dataset(
    metadata: LegacyDatasetMetadata,
    acquisition_id: Optional[int] = None,
    sample_id: Optional[int] = None,
    pub_tables: List[PublicationTable] = [],
) -> DatasetTable:

    dataset = DatasetTable(
        name=metadata.id,
        description=metadata.title,
        institutions=metadata.institution,
        software_availability=metadata.softwareAvailability,
        acquisition_id=acquisition_id,
        sample_id=sample_id,
        publications=pub_tables,
        published=True,
        thumbnail_url=metadata.thumbnailURL,
    )
    return dataset


def legacy_create_view(
    metadata: LegacyView, dataset: DatasetTable, images: List[ImageTable]
) -> ViewTable:
    view = ViewTable(
        name=metadata.name,
        dataset_name=dataset.name,
        description=metadata.description,
        position=metadata.position,
        scale=metadata.scale,
        orientation=metadata.orientation,
        sources=images,
    )
    return view


def ingest_dataset(blob: Dict[str, any], session: Session):
    dmeta = DatasetManifest(**blob)

    session.query(DatasetTable).where(DatasetTable.name == dmeta.name).delete()

    # generate the acquisition table
    acq_model = dmeta.metadata.imaging
    sample_model = dmeta.metadata.sample

    acq_table = legacy_create_acquisition(acq_model)
    sample_table = legacy_create_sample(sample_model)

    pub_tables = [legacy_create_pub(d, type="DOI") for d in dmeta.metadata.DOI]
    pub_tables.extend(
        [legacy_create_pub(d, type="paper") for d in dmeta.metadata.publications]
    )
    session.add_all([acq_table, sample_table, *pub_tables])

    dataset = legacy_create_dataset(
        dmeta.metadata,
        acquisition_id=acq_table.id,
        sample_id=sample_table.id,
        pub_tables=pub_tables,
    )
    session.add(dataset)
    session.commit()
    image_tables: Dict[str, VolumeTable] = {}

    for value in dmeta.sources.values():
        display_settings = DisplaySettings(
            contrast_limits=ContrastLimits(
                **value.displaySettings.contrastLimits.dict()
            ),
            invert_lut=value.displaySettings.invertLUT,
            color=value.displaySettings.color,
        )
        image_tables[value.name] = ImageTable(
            name=value.name,
            description=value.description,
            url=value.url,
            display_settings=display_settings.dict(),
            format=value.format,
            transform=value.transform.dict(),
            sample_type=value.sampleType,
            content_type=value.contentType,
            dataset_name=dataset.name,
        )

    session.add_all(list(image_tables.values()))
    view_tables = []
    for v in dmeta.views:
        view_image_names = v.sources
        view_images = [v for k, v in image_tables.items() if k in view_image_names]
        view_tables.append(legacy_create_view(v, dataset, images=view_images))
    session.add_all(view_tables)
    session.commit()
    return (acq_table, sample_table, *pub_tables, dataset, image_tables, view_tables)


def main(SessionLocal):
    blobs = get_json()
    with SessionLocal() as session:
        for blob in blobs:
            print_json(data=blob)
            tables = ingest_dataset(blob, session=session)


if __name__ == "__main__":
    main(SessionLocal)
