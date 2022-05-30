from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import association_proxy

view_to_volume = Table(
    "view_to_volume",
    Base.metadata,
    Column("view_id", ForeignKey("view.id"), primary_key=True),
    Column("volume_id", ForeignKey("volume.id"), primary_key=True),
)


class ViewTable(Base):
    __tablename__ = "view"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    dataset_name = Column(
        String, ForeignKey("dataset.name"), nullable=False, index=True
    )
    description = Column(String)
    sources = relationship("VolumeTable", secondary=view_to_volume, lazy="joined")
    source_names = association_proxy("sources", "name")
    position = Column(postgresql.ARRAY(Float))
    scale = Column(Float)
    orientation = Column(postgresql.ARRAY(Float))
