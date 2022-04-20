from typing import Dict

from sqlmodel import SQLModel


class Index(SQLModel):
    """
    Store the mapping from dataset IDs to paths to dataset metadata
    """
    datasets: Dict[str, str]
