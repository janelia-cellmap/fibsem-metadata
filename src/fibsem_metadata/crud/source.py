from fibsem_metadata.models.source import VolumeCreate, VolumeUpdate
from fibsem_metadata.schemas.source import VolumeTable

from .base import Base


class VolumeCRUD(Base[VolumeTable, VolumeCreate, VolumeUpdate]):
    pass


volume_crud = VolumeCRUD(VolumeTable)
