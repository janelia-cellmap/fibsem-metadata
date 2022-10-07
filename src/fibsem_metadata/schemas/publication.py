from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .base import Base

pub_to_dataset = Table(
    "publication_to_dataset",
    Base.metadata,
    Column(
        "publication_id",
        ForeignKey("publication.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    ),
    Column(
        "dataset_id",
        ForeignKey("dataset.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    ),
)


class PublicationTable(Base):
    __tablename__ = "publication"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    type = Column(String)
    url = Column(String)
    datasets = relationship(
        "DatasetTable",
        secondary=pub_to_dataset,
        back_populates="publications",
    )
