from .base import Base


class Sample(Base):
    """
    Metadata describing the sample and sample preparation.
    """

    description: str
    protocol: str
    contributions: str
    organism: list[str]
    type: list[str]
    subtype: list[str]
    treatment: list[str]
