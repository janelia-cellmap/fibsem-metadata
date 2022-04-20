from typing import TYPE_CHECKING
from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .metadata import Dataset

class View(SQLModel, table=True):
    id: int | None = Field()
    name: str
    description: str
    dataset: Dataset = Relationship(back_populates="views")
    sources: list[str]
    position: list[str] | None
    scale: float | None
    orientation: list[float] | None

    @validator("orientation")
    def orientation_must_have_unit_norm(
        cls, v: list[float] | None
    ) -> list[float] | None:
        if v is not None:
            if len(v) != 4:
                raise ValueError(
                    f"Orientation must have length 4, got {v} with {len(v)}"
                )
            length = sum([x ** 2 for x in v]) ** 0.5
            if length % 1.0 != 0:
                raise ValueError(
                    "Orientation vector does not have a unit length. Got {length}."
                )
        return v