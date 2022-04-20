from typing import List

from sqlmodel import SQLModel
from .sources import ContentTypeEnum


class ClassMetadata(SQLModel):
    description: str
    contentTypes: List[ContentTypeEnum]
    color: str
