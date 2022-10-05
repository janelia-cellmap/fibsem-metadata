from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from .base import Base

view_to_image = Table(
    "view_to_image",
    Base.metadata,
    Column("view_id", ForeignKey("view.id"), primary_key=True, index=True),
    Column("image_id", ForeignKey("image.id"), primary_key=True, index=True),
)


class ViewTable(Base):
    __tablename__ = "view"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    dataset_name = Column(
        String, ForeignKey("dataset.name"), nullable=False, index=True
    )
    description = Column(String)
    sources = relationship("ImageTable", secondary=view_to_image)
    source_names = association_proxy("sources", "name")
    position = Column(postgresql.ARRAY(Float))
    scale = Column(Float)
    orientation = Column(postgresql.ARRAY(Float))
