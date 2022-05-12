from sqlalchemy.orm import Session
from fastapi import FastAPI, APIRouter, Depends, Query, Request, HTTPException
from fibsem_metadata.crud import base
from fibsem_metadata.schemas.dataset import DatasetTable
from fibsem_metadata.session import get_db
from fibsem_metadata import models, schemas
from fibsem_metadata.crud import dataset_crud, volume_crud

app = FastAPI(title='FIBSEM Metadata', openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get('/datasets/{dataset_name}', status_code=200, response_model=models.Dataset)
def get_dataset_by_name(*,
                 name: str,
                 db: Session = Depends(get_db)) -> list[schemas.DatasetTable]:
    result = db.query(dataset_crud.model).filter(dataset_crud.model.name == name).first()
    if not result: 
        raise HTTPException(status_code=404, detail=f"Dataset with name {name} was not found.")
    return result


@api_router.get('/datasets/{dataset_name}/volumes/{volume_name}', status_code=200, response_model=models.Volume)
def get_dataset_by_name(*,
                 dataset_name: str,
                 volume_name: str,
                 db: Session = Depends(get_db)) -> schemas.VolumeTable:
    result = db.query(volume_crud.model).filter(volume_crud.model.name == volume_name, volume_crud.model.dataset_name == dataset_name).filter().first()
    if not result: 
        raise HTTPException(status_code=404, detail=f"Unable to find a volume named {volume_name} associated with a dataset named {dataset_name}.")
    return result


app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
