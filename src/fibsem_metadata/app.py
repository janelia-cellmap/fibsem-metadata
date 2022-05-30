from sqlalchemy.orm import Session
from fastapi import FastAPI, APIRouter, Depends, Query, HTTPException
from fibsem_metadata.session import get_db
from fibsem_metadata import models, schemas
from fibsem_metadata.crud import dataset_crud
from sqlalchemy.orm import joinedload
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FIBSEM Metadata", openapi_url="/openapi.json")

origins = ["*"]

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)

api_router = APIRouter()


@api_router.get(
    "/datasets/",
    status_code=200,
    response_model=list[models.Dataset],
    response_model_exclude_none=True,
)
def get_datasets(
    *, skip: int = 0, limit: int | None = None, db: Session = Depends(get_db)
) -> list[schemas.DatasetTable]:
    result = dataset_crud.get_multi(db, skip=skip, limit=limit)

    if not result:
        raise HTTPException(status_code=404, detail=f"Error retrieving datasets.")
    return result


@api_router.get(
    "/datasets/{dataset_name}", status_code=200, response_model=models.Dataset
)
def get_dataset_by_name(
    *, dataset_name: str, db: Session = Depends(get_db)
) -> schemas.DatasetTable:

    query = db.query(dataset_crud.model).filter(dataset_crud.model.name == dataset_name)
    result = query.first()
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Dataset with name {dataset_name} was not found."
        )
    return result


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
