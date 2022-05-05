from .base import Base
from sqlalchemy import Column, relationship, String, ForeignKey, Table, Integer

pub_to_dataset = Table(
    "publication_to_dataset",
    Base.metadata,
    Column("publication_id", ForeignKey("publication.id"), primary_key=True),
    Column("dataset_id", ForeignKey("dataset.id"), primary_key=True),
)

class PublicationTable(Base):
    __tablename__ = "publication"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    type = Column(String)
    url = Column(String)
    datasets = relationship(
        "DatasetTable", secondary=pub_to_dataset, back_populates="publications"
    )