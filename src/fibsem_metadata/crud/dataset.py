from typing import List, Optional
from fibsem_metadata.models.dataset import DatasetCreate, DatasetRead, DatasetUpdate
from fibsem_metadata.schemas.dataset import DatasetTable
from sqlalchemy.orm import Session, selectinload, joinedload, subqueryload

from fibsem_metadata.schemas.source import ImageTable
from fibsem_metadata.schemas.view import ViewTable
from .base import Base


class DatasetCRUD(Base[DatasetTable, DatasetCreate, DatasetUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[DatasetTable]:
        return (
            db.query(self.model)
            .options(selectinload("*"))
            .filter(self.model.name == name)
            .first()
        )

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: Optional[int] = None
    ) -> List[DatasetTable]:
        return (
            db.query(self.model)
            .options(selectinload("*"))
            .offset(skip)
            .limit(limit)
            .all()
        )


dataset_crud = DatasetCRUD(DatasetTable)
