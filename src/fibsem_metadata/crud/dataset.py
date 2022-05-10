from fibsem_metadata.schemas.dataset import DatasetTable
from .base import Base
from fibsem_metadata.models.dataset import Dataset, DatasetCreate, DatasetUpdate, DatasetRead

class DatasetCRUD(Base[Dataset, DatasetCreate, DatasetUpdate]):
    pass

dataset_crud = DatasetCRUD(DatasetTable)