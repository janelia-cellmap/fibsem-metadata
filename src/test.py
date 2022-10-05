from ntpath import join
from select import select
from fibsem_metadata.models.dataset import DatasetRead
from fibsem_metadata.schemas.dataset import DatasetTable
from fibsem_metadata.db.session import (
    engine,
    sessionmaker,
    json_serializer,
    create_engine,
)
from fibsem_metadata.core.config import settings
from time import time
from sqlalchemy.orm import joinedload, selectinload, subqueryload

start = time()
engine = create_engine(
    settings.db_uri(),
    future=True,
    echo=True,
    json_serializer=json_serializer,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
db = SessionLocal()

start = time()
qry = db.query(DatasetTable).options(selectinload("*"))
qry_sql = str(qry.statement.compile(engine, compile_kwargs={"literal_binds": True}))
print(qry_sql)
results = [DatasetRead.from_orm(result) for result in qry.all()]
print(f"got {len(results)} results from db in {time() - start}s")
