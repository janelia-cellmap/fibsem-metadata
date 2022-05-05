from sqlalchemy import Integer, Column, String, relationship
from sqlalchemy.dialects import postgresql
from .base import Base


class SampleTable(Base):
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True, autoincrement=True)
    organism = Column(postgresql.ARRAY(String))
    type = Column(postgresql.ARRAY(String))
    subtype = Column(postgresql.ARRAY(String))
    treatment = Column(postgresql.ARRAY(String))
    contributions = Column(String)
    datasets = relationship("DatasetTable")
