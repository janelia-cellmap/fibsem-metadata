from sqlmodel import Session, select
from fibsem_metadata.database import create_db_and_tables, engine

from fibsem_metadata.models.dataset import Dataset, DummyChild, FIBSEMAcquisition, SampleBase, UnitfulVector

def create_dataset():
    with Session(engine) as session:
        gridspacing = UnitfulVector(unit='nm', values={'z': 4.0, 'y': 4.0, 'x': 4.0})
        dimensions = UnitfulVector(unit='samples', values={'z': 1000, 'y': 1000, 'x': 1000})
        acquisition = FIBSEMAcquisition(instrument='scope_1',
                                    institution='janelia',
                                    startDate='2020-10-01',
                                    gridSpacing=gridspacing,
                                    dimensions=dimensions,
                                    duration_days=10,
                                    biasVoltage=None,
                                    scanRate=None,
                                    current=None,
                                    primaryEnergy=None)
        create_db_and_tables()
        session.add(acquisition)
        session.commit()

        child = DummyChild(acquisition=acquisition, acquistion_id=acquisition.id)
        session.add(child)
        session.commit()

        query = select(DummyChild)
        result = session.exec(query)
        for r in result:
            print(r)


if __name__ == '__main__':
    create_dataset()

def foo():
    sample = SampleBase(description='the sample',
                            protocol='protocol',
                            contributions='contributions',
                            organism=['organism'],
                            type=[],
                            subtype=[],
                            treatment=[],
                            institution=[])

    dataset = Dataset(name='foo',
                        description='bar',
                        acquisition_id=None,
                        acquisition=acquisition,
                        sample=sample, 
                        views=[],
                        institution=[],
                        softwareAvailability="open",
                        doi=[],
                        publications=[])
    create_db_and_tables()
    session.add(acquisition)
    session.commit()