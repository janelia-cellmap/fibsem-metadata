from sqlmodel import Relationship
from .base import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Float, Table, null
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql


class DataSourceMixin:
    name = Column(String, index=True)
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


view_to_volume = Table('view_to_volume',
                        Base.metadata,
                        Column("view_id", ForeignKey('view.id'), primary_key=True),
                        Column("volume_id", ForeignKey('volume.id'), primary_key=True))



pub_to_dataset = Table('publication_to_dataset',
                        Base.metadata,
                        Column("publication_id", ForeignKey('publication.id'), primary_key=True),
                        Column("dataset_id", ForeignKey('dataset.id'), primary_key=True))


class Publication(Base):
    __tablename__ = "publication"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    type = Column(String)
    url = Column(String)
    datasets = relationship("Dataset",
                            secondary=pub_to_dataset,
                            back_populates="publications")


class DisplaySettings(Base):
    __tablename__ = 'displaysettings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(String)
    invertLUT = Column(Boolean)
    contrast_limits_start = Column(Integer)
    contrast_limits_end = Column(Integer)
    contrast_limits_min = Column(Integer)
    contrast_limits_max = Column(Integer)


class Mesh(Base, DataSourceMixin):
    __tablename__ = 'mesh'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    volume_id = Column(Integer, ForeignKey("volume.id"))
    volume = relationship("Volume")


class Volume(Base, DataSourceMixin):
    __tablename__ = 'volume'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_type = Column(String)
    content_type = Column(String)
    views = relationship("View", secondary=view_to_volume, back_populates="sources")
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)
    dataset = relationship("Dataset", back_populates="volumes")
    subsources = relationship("Mesh", back_populates="volume")


class View(Base):
    __tablename__ = 'view'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    sources = relationship("Volume", secondary=view_to_volume, back_populates="views")
    position = Column(postgresql.ARRAY(Float))
    orientation = Column(postgresql.ARRAY(Float))


class LabelClass(Base):
    __tablename__ = "labelclass"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    value = Column(Integer)
    annotation_state = Column(postgresql.JSONB)
    crop_id = Column(Integer, ForeignKey("crop.id"), nullable=False)
    crop = relationship("Crop")


class Crop(Base):
    __tablename__ = "crop"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    source_id = Column(ForeignKey('volume.id'), nullable=False)
    annotations = relationship(LabelClass, back_populates='crop')
    shape = Column(postgresql.ARRAY(Integer))
    completion_stage = Column(String, index=True)
    transform_world = Column(postgresql.JSONB)
    transform_source = Column(postgresql.JSONB)


class Sample(Base):
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True, autoincrement=True)
    organism = Column(postgresql.ARRAY(String))
    type = Column(postgresql.ARRAY(String))
    subtype = Column(postgresql.ARRAY(String))
    treatment = Column(postgresql.ARRAY(String))
    contributions = Column(String)
    datasets = relationship("Dataset")


class FIBSEMAcquisition(Base, ImageAcquisitionMixin):
    __tablename__ = 'fibsem_acquisition'

    id = Column(Integer, primary_key=True, autoincrement=True)
    duration_days = Column(Integer)
    bias_voltage = Column(Float)
    scan_rate = Column(Float)
    current = Column(Float)
    primary_energy = Column(Float)
    datasets = relationship("Dataset")


class Dataset(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

    institution = Column(postgresql.ARRAY(String))
    software_availability = Column(String)

    volumes = relationship(Volume, back_populates="dataset")

    acquisition_id = Column(Integer, ForeignKey("fibsem_acquisition.id"), nullable=False)
    acquisition = relationship(FIBSEMAcquisition, back_populates="datasets")

    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    sample = relationship(Sample, back_populates="datasets")

    publications = relationship(Publication,
                                secondary=pub_to_dataset,
                                back_populates="datasets")