from typing import List, Optional, Any

from pydantic import validator
from sqlalchemy.ext.associationproxy import _AssociationList

from .base import Base


class View(Base):
    name: str
    description: str
    sourceNames: List[str]
    position: Optional[List[float]]
    scale: Optional[float]
    orientation: Optional[List[float]]

    @validator("source_names", pre=True)
    def listify_association_proxy(cls, v: Any) -> List[str]:
        """
        Convert a list-like sqlalchemy association proxy into a list
        """
        if isinstance(v, _AssociationList):
            return list(v)
        return v

    @validator("orientation")
    def orientation_must_have_unit_norm(
        cls, v: Optional[List[float]]
    ) -> Optional[List[float]]:
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
