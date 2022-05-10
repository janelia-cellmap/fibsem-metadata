from .base import Base
from sqlalchemy import JSON, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql


class DataSourceMixin:
    name = Column(String, index=True)
    description = Column(String)
    url = Column(String)
    format = Column(String)
    transform = Column(postgresql.JSONB)


class DisplaySettingsTable(Base):
    __tablename__ = "displaysettings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(String)
    invertLUT = Column(Boolean)
    contrast_limits = Column(postgresql.JSONB)


class MeshTable(Base, DataSourceMixin):
    __tablename__ = "mesh"

    id = Column(Integer, primary_key=True, autoincrement=True)
    volume_id = Column(Integer, ForeignKey("volume.id"))
    volume = relationship("VolumeTable")


class VolumeTable(Base, DataSourceMixin):
    __tablename__ = "volume"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_type = Column(String)
    content_type = Column(String)
    display_settings = Column(postgresql.JSONB)
    views = relationship(
        "ViewTable", secondary="view_to_volume", back_populates="sources"
    )
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)
    dataset = relationship("DatasetTable", back_populates="volumes")
    subsources = relationship("MeshTable", back_populates="volume")
