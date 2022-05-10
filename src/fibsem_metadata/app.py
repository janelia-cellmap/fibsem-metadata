from sqlalchemy.orm import Session
from fastapi import FastAPI, APIRouter, Depends, Query, Request, HTTPException
from fibsem_metadata.crud import base
from fibsem_metadata.session import get_db
from fibsem_metadata import models
from fibsem_metadata.crud.dataset import dataset_crud

app = FastAPI(title='FIBSEM Metadata', openapi_url="/openapi.json")

api_router = APIRouter()

@api_router.get('/datasets/', status_code=200, response_model=list[models.dataset.DatasetRead])
def get_datasets(*,
                 limit: int = 1,
                 db: Session = Depends(get_db)) -> list[models.Dataset]:
    result = dataset_crud.get_multi(db=db, limit=limit)
    return result 

app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
