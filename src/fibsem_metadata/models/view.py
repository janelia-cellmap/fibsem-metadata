from sqlalchemy.ext.associationproxy import _AssociationList
from pydantic import validator

from fibsem_metadata.models.source import Volume
from .base import Base


class View(Base):
    name: str
    description: str
    source_names: list[str]
    position: list[float] | None
    scale: float | None
    orientation: list[float] | None

    @validator("source_names", pre=True)
    def listify_association_proxy(cls, v):
        """
        Convert a list-like sqlalchemy association proxy into a list
        """
        if isinstance(v, _AssociationList):
            return list(v)
        return v

    @validator("orientation")
    def orientation_must_have_unit_norm(
        cls, v: list[float] | None
    ) -> list[float] | None:
        if v is not None:
            if len(v) != 4:
                raise ValueError(
                    f"Orientation must have length 4, got {v} with {len(v)}"
                )
            length = sum([x**2 for x in v]) ** 0.5
            if length % 1.0 != 0:
                raise ValueError(
                    "Orientation vector does not have a unit length. Got {length}."
                )
        return v

class ViewRead(View):
    id: int
