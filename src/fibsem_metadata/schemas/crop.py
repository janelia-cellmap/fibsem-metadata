from sqlalchemy import Column, Integer, String, ForeignKey, relationship
from sqlalchemy.dialects import postgresql
from .base import Base


class LabelClassTable(Base):
    __tablename__ = "labelclass"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    value = Column(Integer)
    annotation_state = Column(postgresql.JSONB)
    crop_id = Column(Integer, ForeignKey("crop.id"), nullable=False)
    crop = relationship("CropTable")


class CropTable(Base):
    __tablename__ = "crop"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    description = Column(String, index=True)
    source_id = Column(ForeignKey("volume.id"), nullable=False)
    annotations = relationship(LabelClassTable, back_populates="crop")
    shape = Column(postgresql.ARRAY(Integer))
    completion_stage = Column(String, index=True)
    transform_world = Column(postgresql.JSONB)
    transform_source = Column(postgresql.JSONB)
