from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import fibsem_metadata.models as models
import fibsem_metadata.schemas as schemas
from fibsem_metadata import crud
from fibsem_metadata.api import deps

router = APIRouter()


@router.get(
    "/",
    status_code=200,
    response_model=List[models.Dataset],
    response_model_exclude_none=True,
)
def get_datasets(
    *, skip: int = 0, limit: Optional[int] = None, db: Session = Depends(deps.get_db)
) -> List[schemas.DatasetTable]:
    result = crud.dataset_crud.get_multi(db, skip=skip, limit=limit)
    if not result:
        raise HTTPException(status_code=404, detail="Error retrieving datasets.")
    return result


@router.get("/{dataset_name}", status_code=200, response_model=models.Dataset)
def get_dataset_by_name(
    *, dataset_name: str, db: Session = Depends(deps.get_db)
) -> schemas.DatasetTable:
    crud_class = crud.dataset_crud
    query = db.query(crud_class.model).filter(crud_class.model.name == dataset_name)
    result = query.first()
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Dataset with name {dataset_name} was not found."
        )
    return result
