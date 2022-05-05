from .base import Base
from sqlalchemy import Column, Integer, String, relationship, ForeignKey


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
    views = relationship(
        "ViewTable", secondary=view_to_volume, back_populates="sources"
    )
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)
    dataset = relationship("DatasetTable", back_populates="volumes")
    subsources = relationship("MeshTable", back_populates="volume")
