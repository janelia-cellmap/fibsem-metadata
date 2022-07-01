from typing import Literal
from sqlalchemy.orm import Session
from fibsem_metadata.models import (
    Dataset,
    View,
    Sample,
    FIBSEMAcquisition,
)
from fibsem_metadata.models.acquisition import UnitfulVector
from fibsem_metadata.models.source import DisplaySettings, Volume
from fibsem_metadata.legacy_models.manifest import DatasetManifest
import json
from glob import glob
from fibsem_metadata.schemas import (
    DatasetTable,
    PublicationTable,
    VolumeTable,
    ViewTable,
    SampleTable,
    FIBSEMAcquisitionTable,
)


def create_sample(metadata: Sample) -> SampleTable:
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


def create_acquisition(
    metadata: FIBSEMAcquisition,
    instrument: str = "",
    grid_shape: dict[str, int] = {"z": 0, "z": 0, "x": 0},
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


def create_pub(metadata, type: Literal["DOI", "publication"]) -> PublicationTable:

    pub = PublicationTable(name=metadata.title, url=metadata.href, type=type.lower())
    return pub


def create_dataset(
    metadata: Dataset,
    acquisition_id: int | None = None,
    sample_id: int | None = None,
    pub_tables: list[PublicationTable] = [],
) -> DatasetTable:

    dataset = DatasetTable(
        name=metadata.id,
        description=metadata.title,
        institutions=metadata.institution,
        software_availability=metadata.softwareAvailability,
        acquisition_id=acquisition_id,
        sample_id=sample_id,
        publications=pub_tables,
    )
    return dataset


def create_view(
    metadata: View, dataset: DatasetTable, volumes: list[VolumeTable]
) -> ViewTable:
    view = ViewTable(
        name=metadata.name,
        dataset_name=dataset.name,
        description=metadata.description,
        position=metadata.position,
        scale=metadata.scale,
        orientation=metadata.orientation,
        sources=volumes,
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
    volume_tables: dict[str, VolumeTable] = {}

    for value in dmeta.sources.values():
        display_settings = DisplaySettings(
            contrast_limits=value.displaySettings.contrastLimits,
            invert_lut=value.displaySettings.invertLUT,
            color=value.displaySettings.color,
        )
        volume_tables[value.name] = VolumeTable(
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

    session.add_all(list(volume_tables.values()))
    session.commit()
    view_tables = []
    for v in dmeta.views:
        view_volume_names = v.sources
        view_volumes = [v for k, v in volume_tables.items() if k in view_volume_names]
        view_tables.append(create_view(v, dataset, volumes=view_volumes))
    session.add_all(view_tables)
    session.commit()
    return acq_table, sample_table, *pub_tables, dataset, volume_tables, view_tables


if __name__ == "__main__":
    with Session(engine) as session:
        paths = glob("api/*/manifest.json")
        for path in paths:
            tables = ingest_dataset(path, session=session)
