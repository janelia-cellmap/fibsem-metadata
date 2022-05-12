from fibsem_metadata.schemas.dataset import DatasetTable
from .base import Base
from fibsem_metadata.models.dataset import DatasetCreate, DatasetUpdate, DatasetRead

class DatasetCRUD(Base[DatasetTable, DatasetCreate, DatasetUpdate]):
    pass

dataset_crud = DatasetCRUD(DatasetTable)