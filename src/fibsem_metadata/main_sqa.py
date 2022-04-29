from turtle import position
from typing import Literal
from sqlalchemy.orm import Session
from fibsem_metadata.database_sqa import create_db_and_tables, engine
import fibsem_metadata.schemas.views as schemas
from fibsem_metadata.models.metadata import (
    DatasetMetadata,
    Hyperlink,
    SampleMetadata,
    FIBSEMImagingMetadata,
)
from fibsem_metadata.models.manifest import DatasetManifest, DatasetView
import json
from glob import glob


def create_sample(metadata: SampleMetadata) -> schemas.Sample:
    sample = schemas.Sample(
        organism=metadata.organism,
        type=metadata.type,
        subtype=metadata.subtype,
        treatment=metadata.treatment,
        contributions=metadata.contributions,
    )
    return sample


def create_acquisition(
    metadata: FIBSEMImagingMetadata,
    instrument: str = "",
    grid_shape: list[int] = [0, 0, 0],
    grid_unit: str = "nm",
) -> schemas.FIBSEMAcquisition:

    acq = schemas.FIBSEMAcquisition(
        instrument=instrument,
        institution=metadata.institution,
        start_date=metadata.startDate,
        sampling_grid_unit=grid_unit,
        sampling_grid_spacing=metadata.gridSpacing.values.values(),
        sampling_grid_shape=grid_shape,
        duration_days=metadata.duration,
        bias_voltage=metadata.biasVoltage,
        scan_rate=metadata.scanRate,
        current=metadata.current,
        primary_energy=metadata.primaryEnergy,
    )

    return acq


def create_pub(
    metadata: Hyperlink, type: Literal["DOI", "publication"]
) -> schemas.Publication:

    pub = schemas.Publication(name=metadata.title, url=metadata.href, type=type)
    return pub


def create_dataset(
    metadata: DatasetMetadata,
    acquisition_id: int | None = None,
    sample_id: int | None = None,
    pub_tables: list[schemas.Publication] = [],
) -> schemas.Dataset:

    dataset = schemas.Dataset(
        name=metadata.id,
        description=metadata.title,
        institution=metadata.institution,
        software_availability=metadata.softwareAvailability,
        acquisition_id=acquisition_id,
        sample_id=sample_id,
        publications=pub_tables,
    )
    return dataset


def create_view(metadata: DatasetView, dataset: schemas.Dataset) -> schemas.View:
    sources = []
    names = [d.name for d in dataset.volumes]
    for k in metadata.sources:
        if k in names:
            sources.append(dataset.volumes[names.index(k)])

    view = schemas.View(
        name=metadata.name,
        description=metadata.description,
        sources=sources,
        position=metadata.position,
        orientation=metadata.orientation,
        dataset_id=dataset.id,
        dataset=dataset,
    )
    return view


def ingest_dataset(path, session: Session):
    results = []
    with open(path) as fh:
        blob = json.load(fh)
    dmeta = DatasetManifest(**blob)

    # generate the acquisition table
    acq_model = dmeta.metadata.imaging
    sample_model = dmeta.metadata.sample

    acq_table = create_acquisition(acq_model)
    sample_table = create_sample(sample_model)

    pub_tables = [create_pub(d, type="DOI") for d in dmeta.metadata.DOI]
    pub_tables.extend(
        [create_pub(d, type="paper") for d in dmeta.metadata.publications]
    )

    session.add_all([acq_table, sample_table, *pub_tables])
    session.commit()

    dataset = create_dataset(
        dmeta.metadata,
        acquisition_id=acq_table.id,
        sample_id=sample_table.id,
        pub_tables=pub_tables,
    )

    session.add(dataset)
    session.commit()
    volume_tables: dict[str, schemas.Volume] = {}

    for value in dmeta.sources.values():
        volume_tables[value.name] = schemas.Volume(
            name=value.name,
            description=value.description,
            url=value.url,
            format=value.format,
            transform=value.transform.json(),
            sample_type=value.sampleType,
            content_type=value.contentType,
            dataset_id=dataset.id,
        )

    session.add_all(list(volume_tables.values()))
    session.commit()

    view_tables = [create_view(v, dataset) for v in dmeta.views]
    session.add_all(view_tables)
    session.commit()
    return acq_table, sample_table, *pub_tables, dataset, volume_tables, view_tables


if __name__ == "__main__":
    create_db_and_tables(engine, wipe=True)
    with Session(engine) as session:
        paths = glob("api/*/manifest.json")
        for path in paths:
            tables = ingest_dataset(path, session=session)
