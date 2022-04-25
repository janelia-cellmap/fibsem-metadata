from sqlmodel import Session, select
from fibsem_metadata.database import create_db_and_tables, engine
from fibsem_metadata.models.sources import DisplaySettings, DisplaySettingsBase, Volume, VolumeBase
from fibsem_metadata.models.dataset import Dataset, FIBSEMAcquisition, Sample, UnitfulVector
from fibsem_metadata.models.views import View, ViewBase

def create_view():
    with Session(engine) as session:
        create_db_and_tables(wipe=True)
        displayb = DisplaySettingsBase(contrastLimits={'start': 0, 'end': 10, 'min': 0, 'max': 10}, color='white', invertLUT=False)
        display = DisplaySettings.from_orm(displayb)
        
        session.add(display)
        session.commit()
        
        sourceb = Volume(name='fibsem-uint8',
                        description='a nice dataset',
                        url='s3://janelia-cosem-datasets/jrc_hela-2/jrc_hela-2.n5/em/fibsem-uint8',
                        sampleType='scalar',
                        contentType='em',
                        format='n5',
                        transform={'axes': ['z','y','x'], 'units': ['nm','nm','nm'], 'scale': [4.0, 4.0, 4.0], 'translate': [0,0,0]},
                        displaySettings_id=display.id)
        
        source = sourceb        
        session.add(source)
        session.commit()

        viewb = ViewBase(name='default view',
                    description='hello',
                    sources = ['fibsem-uint8'],
                    position=[3.0,3.0,3.0],
                    orientation=[1,0,0,0],
                    scale=1.0)
        
        view  = View.from_orm(viewb)
        session.add(view)
        session.commit()


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

        sample = Sample(description='the sample',
                                protocol='protocol',
                                contributions='contributions',
                                organism=['organism'],
                                type=[],
                                subtype=[],
                                treatment=[],
                                institution=[])


        dataset = Dataset(name='foo',
                        description='bar',
                        acquisition=acquisition,
                        sample=sample, 
                        views=[view],
                        institution=[],
                        softwareAvailability="open",
                        doi=[],
                        publications=[])

        create_db_and_tables()
        session.add(acquisition)
        session.commit()
        session.add(sample)
        session.commit()
        session.add(dataset)
        session.commit()


if __name__ == '__main__':
    create_view()