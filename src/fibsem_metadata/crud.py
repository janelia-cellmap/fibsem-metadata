from sqlalchemy import Session

import fibsem_metadata.schemas.views as schemas
import fibsem_metadata.models as models
from sqlalchemy import Session


def get_dataset_by_id(db: Session, id: int) -> models.dataset.Dataset:
    return db.query(schemas.Dataset).get(id)


def get_dataset_by_name(db: Session, name: str) -> models.dataset.Dataset:
    return db.query(schemas.Dataset).filter(schemas.Dataset.name == name).first()


def get_datasets(db: Session, limit: int = 100) -> list[models.dataset.Dataset]:
    return  db.query(schemas.Dataset).limit(limit).all()