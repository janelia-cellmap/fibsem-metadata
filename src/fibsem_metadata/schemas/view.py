from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

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
    description = Column(String)
    sources = relationship(
        "VolumeTable", secondary=view_to_volume, back_populates="views"
    )
    position = Column(postgresql.ARRAY(Float))
    orientation = Column(postgresql.ARRAY(Float))
    dataset_id = Column(Integer, ForeignKey("dataset.id"), nullable=False)
    dataset = relationship("DatasetTable", back_populates="views")
