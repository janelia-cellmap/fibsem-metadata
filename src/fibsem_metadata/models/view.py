from pydantic import validator
from .source import Volume
from .base import Base


class View(Base):
    name: str
    description: str
    sources: list[Volume]
    position: list[float] | None
    scale: list[float] | None
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
            length = sum([x**2 for x in v]) ** 0.5
            if length % 1.0 != 0:
                raise ValueError(
                    "Orientation vector does not have a unit length. Got {length}."
                )
        return v
