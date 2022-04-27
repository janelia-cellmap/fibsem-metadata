from sqlalchemy.orm import Session
from fibsem_metadata.database_sqa import create_db_and_tables, engine
import fibsem_metadata.schemas.views as schemas
from fibsem_metadata.models.manifest import DatasetManifest
import json

def ingest_dataset(path):
    with open(path) as fh:
        blob = json.load(fh)
    dmeta = DatasetManifest(**blob)
    
    # generate the acquisition table
    acq_model = dmeta.metadata.imaging
    acq_table = schemas.FIBSEMAcquisition(instrument="",
                                        institution=acq_model.institution,
                                        start_date=acq_model.startDate,
                                        sampling_grid_unit='nm',
                                        sampling_grid_spacing=acq_model.gridSpacing.values.values(),
                                        sampling_grid_shape=[10,10,10],
                                        duration_days=acq_model.duration,
                                        bias_voltage=acq_model.biasVoltage,
                                        scan_rate=acq_model.scanRate,
                                        current=acq_model.current,
                                        primary_energy=acq_model.primaryEnergy)

    return acq_table



if __name__ == '__main__':
    create_db_and_tables(engine, wipe=True)
    with Session(engine) as session:
        table = ingest_dataset('api/jrc_hela-2/manifest.json')
        session.add_all([table])
        session.commit()

