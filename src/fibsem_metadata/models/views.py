from typing import TYPE_CHECKING
from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .dataset import Dataset


class ViewBase(SQLModel):
    name: str
    description: str
    dataset: "Dataset"
    sources: list[str]
    position: list[str] | None
    scale: float | None
    orientation: list[float] | None = [1, 0, 0, 0]

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
                    "Orientation vector does not have a unit norm. Got {length}."
                )
        return v


class View(ViewBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    dataset: Dataset = Relationship(back_populates="views")