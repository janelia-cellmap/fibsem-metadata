from sqlmodel import SQLModel, create_engine

db_url = "postgresql://admin:admin@localhost:5432/fibsem_metadata"

engine = create_engine(db_url, echo=True)


def create_db_and_tables(wipe=False):
    if wipe:
        SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
