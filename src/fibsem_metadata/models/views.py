from typing import Optional, Sequence
from pydantic import BaseModel, validator


class DatasetView(BaseModel):
    name: str
    description: str
    position: Optional[Sequence[float]]
    scale: Optional[float]
    orientation: Optional[Sequence[float]]
    volumeNames: Sequence[str]

    @validator("orientation")
    def orientation_must_have_unit_norm(
        cls, v: Optional[Sequence[float]]
    ) -> Optional[Sequence[float]]:
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


class DatasetViews(BaseModel):
    views: Sequence[DatasetView]
