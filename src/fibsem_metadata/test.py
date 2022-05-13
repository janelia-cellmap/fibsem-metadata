from fibsem_metadata.models.dataset import Dataset, DatasetRead
from fibsem_metadata.schemas.dataset import DatasetTable

if __name__ == "__main__":

    d = Dataset(
        name="foo",
        description="foo",
        institutions=["hhmi"],
        software_availability="open",
        acquisition=None,
        sample=None,
        publications=[],
        volumes=[],
        views=[],
    )

    d_t = DatasetTable(**d.dict())
    d_t.id = 0
    rt = DatasetRead.from_orm(d_t)
