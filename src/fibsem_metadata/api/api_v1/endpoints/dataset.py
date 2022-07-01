from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from fibsem_metadata import crud
from fibsem_metadata.api import deps

import fibsem_metadata.models as models
import fibsem_metadata.schemas as schemas

router = APIRouter()

@router.get("/datasets/",
            status_code=200,
            response_model=list[models.Dataset],
            response_model_exclude_none=True)
def get_datasets(*, 
                skip: int = 0,
                limit: int | None = None,
                db: Session = Depends(deps.get_db)) -> list[schemas.DatasetTable]:
    result = crud.dataset_crud.get_multi(db, skip=skip, limit=limit)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Dataset with name {dataset_name} was not found."
        )
