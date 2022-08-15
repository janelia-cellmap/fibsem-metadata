from fastapi import APIRouter

from fibsem_metadata.api.v1.endpoints import datasets

api_router = APIRouter()
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
