from fibsem_metadata.models.dataset import Dataset, DatasetRead
from fibsem_metadata.schemas.dataset import DatasetTable
from fibsem_metadata.session import SessionLocal
from fibsem_metadata.crud import dataset_crud
from sqlalchemy.orm import joinedload

if __name__ == "__main__":
    dataset_name = "jrc_macrophage-2"
    db = SessionLocal()
    result = (
        db.query(dataset_crud.model)
        .options(joinedload(dataset_crud.model.volumes))
        .filter(dataset_crud.model.name == dataset_name)
        .first()
    )
    output = Dataset.from_orm(result)
    print(output.json(indent=2))
