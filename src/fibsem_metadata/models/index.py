from typing import Sequence

from fibsem_metadata.models.base import StrictBaseModel


class Index(StrictBaseModel):
    datasets: Sequence[str]
