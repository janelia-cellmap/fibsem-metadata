from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from .base import Base


class SampleTable(Base):
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    protocol = Column(String)
    contributions = Column(String)
    organism = Column(postgresql.ARRAY(String))
    type = Column(postgresql.ARRAY(String))
    subtype = Column(postgresql.ARRAY(String))
    treatment = Column(postgresql.ARRAY(String))
    datasets = relationship("DatasetTable")
