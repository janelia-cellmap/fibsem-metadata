from sqlalchemy import create_engine
from .schemas.base import Base

db_url = "postgresql://admin:admin@localhost:5432/fibsem_metadata"

engine = create_engine(db_url, echo=True, future=True)

def create_db_and_tables(wipe=False):
    if wipe:
        Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)
    
