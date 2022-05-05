from typing import Dict

from fibsem_metadata.legacy_models.base import StrictBaseModel


class Index(StrictBaseModel):
    """
    Store the mapping from dataset IDs to paths to dataset metadata
    """

    datasets: Dict[str, str]
