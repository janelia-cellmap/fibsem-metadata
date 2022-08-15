from fibsem_metadata.models.dataset import (DatasetCreate, DatasetRead,
                                            DatasetUpdate)
from fibsem_metadata.schemas.dataset import DatasetTable

from .base import Base


class DatasetCRUD(Base[DatasetTable, DatasetCreate, DatasetUpdate]):
    pass


dataset_crud = DatasetCRUD(DatasetTable)
