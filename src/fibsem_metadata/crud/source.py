from fibsem_metadata.models.source import ImageCreate, ImageUpdate
from fibsem_metadata.schemas.source import ImageTable

from .base import Base


class ImageCRUD(Base[ImageTable, ImageCreate, ImageUpdate]):
    pass


image_crud = ImageCRUD(ImageTable)
