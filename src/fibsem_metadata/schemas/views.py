from sqlmodel import Relationship
from .base import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql


class DataSourceMixin:
    name = Column(Integer, index=True)
    description = Column(String)
    url = Column(String)
    format = Column(String)
    transform = Column(postgresql.JSONB)


class ImageAcquisitionMixin:
    instrument = Column(String)
    institution = Column(String)
    start_date = Column(Date)
    sampling_grid_unit = Column(String)
    sampling_grid_spacing = Column(postgresql.ARRAY(Float))
    sampling_grid_shape = Column(postgresql.ARRAY(Integer))


class ViewtoVolume(Base):
    __tablename__ = 'view_to_volume'
    
    view_id = Column(ForeignKey('view.id'), primary_key=True)
    volume_id = Column(ForeignKey('volume.id'), primary_key=True)


class DOItoDataset(Base):
    __tablename__ = 'doi_to_dataset'

    doi_id = Column(ForeignKey('doi.id'), primary_key=True)
    dataset_id = Column(ForeignKey('dataset.id'), primary_key=True)


class PublicationtoDataset(Base):
    __tablename__ = 'publication_to_dataset'

    publication_id = Column(ForeignKey('publication.id'), primary_key=True)
    dataset_id = Column(ForeignKey('dataset.id'), primary_key=True)


class DOI(Base):
    __tablename__ = "doi"

    id = Column(Integer, primary_key=True) 
    name = Column(String)
    doi = Column(String)
    datasets = relationship("Dataset", secondary=DOItoDataset)


class Publication(Base):
    __tablename__ = "publication"

    id = Column(Integer, primary_key=True) 
    name = Column(String)
    url = Column(String)
    datasets = relationship("Dataset", secondary=PublicationtoDataset)


class DisplaySettings(Base):
    __tablename__ = 'displaysettings'

    id = Column(Integer, primary_key=True)
    color = Column(String)
    invertLUT = Column(Boolean)
    contrast_limits_start = Column(Integer)
    contrast_limits_end = Column(Integer)
    contrast_limits_min = Column(Integer)
    contrast_limits_max = Column(Integer)


class Mesh(Base, DataSourceMixin):
    __tablename__ = 'mesh'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dataset_id = Column(Integer, ForeignKey("dataset.id"))
    dataset = relationship(back_populates="volumes")    
    volume_id = Column(Integer, ForeignKey("volume.id"))
    volume = relationship("Volume", back_populates="volume.subsources")


class Volume(Base, DataSourceMixin):
    __tablename__ = 'volume'

    id = Column(Integer, primary_key=True)
    sample_type = Column(String)
    content_type = Column(String)
    views = relationship("View", secondary="ViewtoVolume", back_populates="sources")
    dataset_id = Column(Integer, ForeignKey("dataset.id"))
    dataset = relationship(back_populates="volumes")
    subsources = relationship("Mesh", back_populates="volume")


class View(Base):
    __tablename__ = 'view'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    sources = relationship("Volume", secondary="ViewtoVolume", back_populates="views")
    position = Column(postgresql.ARRAY(Float))
    orientation = Column(postgresql.ARRAY(Float))


class LabelClass(Base):
    __tablename__ = "labelclass"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    value = Column(Integer)
    annotation_state = Column(postgresql.JSONB)
    crop_id = Column(Integer, ForeignKey("crop.id"))


class Crop(Base):
    __tablename__ = "crop"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    source_id = Column(ForeignKey('volume.id'))
    annotations = relationship("LabelClass", back_populates='crop_id')
    shape = Column(postgresql.ARRAY(Integer))
    completion_stage = Column(String, index=True)
    transform_world = Column(postgresql.JSONB)
    transform_source = Column(postgresql.JSONB)


class Sample(Base):
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True)
    organism = Column(postgresql.ARRAY(String))
    type = Column(postgresql.ARRAY(String))
    subtype = Column(postgresql.ARRAY(String))
    treatment = Column(postgresql.ARRAY(String))
    institution = Column(postgresql.ARRAY(String))
    datasets = relationship("Dataset")


class FIBSEMAcquisition(Base, ImageAcquisitionMixin):
    __tablename__ = 'fibsem_acquisition'

    duration_days = Column(Integer, )
    bias_voltage = Column(Float)
    scan_rate = Column(Float)
    current = Column(Float)
    primary_energy = Column(Float)
    datasets = relationship("Dataset")


class Dataset(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    
    institution = Column(postgresql.ARRAY(String))
    software_availability = Column(String)
    
    volumes = relationship("Volume", back_populates="dataset")
    meshes = relationship("Mesh", back_populates="dataset")

    acquisition_id = Column(Integer, ForeignKey("fibsem_acquisition.id"))
    acquisition = relationship("FIBSEMAcquisition", back_populates="datasets")
    
    sample_id = Column(Integer, ForeignKey("sample.id"))
    sample = relationship("Sample", back_populates="datasets")
    
    doi = relationship("DOI", secondary=DOItoDataset)
    publications = relationship("Publication", secondary=PublicationtoDataset)
    