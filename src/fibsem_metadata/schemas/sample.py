from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

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
