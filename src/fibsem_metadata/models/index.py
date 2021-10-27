from pydantic import BaseModel
from typing import Sequence


class Index(BaseModel):
    datasets: Sequence[str]
