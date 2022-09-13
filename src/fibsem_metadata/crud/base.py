from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, selectinload

import fibsem_metadata.schemas as schemas

SchemaType = TypeVar("SchemaType", bound=schemas.Base)
CreateModelType = TypeVar("CreateModelType", bound=BaseModel)
UpdateModelType = TypeVar("UpdateModelType", bound=BaseModel)


class Base(Generic[SchemaType, CreateModelType, UpdateModelType]):
    def __init__(self, model: Type[SchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `schema`: A SQLAlchemy table
        * `model`: A Pydantic model
        """
        self.model = model

    def get(self, db: Session, id: int) -> Optional[SchemaType]:
        return db.query(self.model).options(selectinload('*')).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: Optional[int] = None
    ) -> List[SchemaType]:
        return db.query(self.model).options(selectinload('*')).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateModelType) -> SchemaType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: SchemaType,
        obj_in: Union[UpdateModelType, Dict[str, Any]]
    ) -> SchemaType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> SchemaType:
        obj: SchemaType = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
