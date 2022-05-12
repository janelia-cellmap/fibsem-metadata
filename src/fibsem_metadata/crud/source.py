from .base import Base
from fibsem_metadata.schemas.source import VolumeTable
from fibsem_metadata.models.source import VolumeCreate, VolumeUpdate

class VolumeCRUD(Base[VolumeTable, VolumeCreate, VolumeUpdate]):
    pass

volume_crud = VolumeCRUD(VolumeTable)