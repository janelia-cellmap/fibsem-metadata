from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from .base import Base


class DataSourceMixin:
    name = Column(String, index=True)
    description = Column(String)
    url = Column(String)
    format = Column(String)
    transform = Column(postgresql.JSONB)


class MeshTable(Base, DataSourceMixin):
    __tablename__ = "mesh"

    id = Column(Integer, primary_key=True, autoincrement=True)
    volume_id = Column(Integer, ForeignKey("volume.id"), index=True)


class VolumeTable(Base, DataSourceMixin):
    __tablename__ = "volume"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    sample_type = Column(String)
    content_type = Column(String)
    display_settings = Column(postgresql.JSONB)
    dataset_name = Column(
        String, ForeignKey("dataset.name"), nullable=False, index=True
    )
    subsources = relationship("MeshTable")


class ContentTypeTable(Base):
    __tablename__ = "content_type"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    description = Column(String)
