from typing import Protocol
from fibsem_metadata.models.index import VolumeSource
from fibsem_metadata.models.dataset import Dataset, ImagingMetadata, SampleMetadata, FIBSEMImagingMetadata, SoftwareAvailability

dataset_id = 'jrc_fly-mb-z0419-20'
title = "Drosophila brain: entire alpha and alpha' lobes of a mushroom body"
sample = SampleMetadata(description="Drosophila mushroom body: The largest tissue sample imaged at 4-nm voxels to date (2021). Entire alpha and alpha' lobes of a 5 day-old adult female  (Genome type: iso Canton S G1 x w1118 iso 5905)",
                        protocol="Chemical Fixation, ORTO-Lead-EPTA staining via progressive lowering of temperature and low temperature staining (PLT-LTS) heavy metal enhancement protocol.",
                        contributions="Sample provided by Zhiyuan Lu (HHMI/Janelia), prepared for imaging by Song Pang (HHMI/Janelia), with imaging by Song Pang (HHMI/Janelia) and C. Shan Xu (HHMI/Janelia), and post-processing by C. Shan Xu (HHMI/Janelia).",
                        organism=["Drosophila"],
                        type=["Tissue"],
                        subtype=["Brain"],
                        treatment=["Wild-type"])

imaging = FIBSEMImagingMetadata(id='Z0419-20-MB',startDate="2020-05-12",
                                duration=60,
                                biasVoltage=0,
                                scanRate=2,
                                current=0.25,
                                primaryEnergy=700,
                                institution='HHMI/Janelia',
                                dimensions={'unit': 'nm', 'values': {'x' : 120, 'y' : 72, 'z' : 105}},
                                gridSpacing={'unit': 'nm', 'values': {'x' : 4.0, 'y' : 4.0, 'z':  4.0}})

meta = Dataset(title=title,
               id=dataset_id,
               imaging=imaging,
               sample=sample,
               institution=["HHMI/Janelia"],
               softwareAvailability="open",
               DOI=[{"id": "EM", "DOI": "10.25378/janelia.16638268"}],
               publications=[])

if __name__ == '__main__':
    print(meta.json(indent=2))