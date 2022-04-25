from enum import Enum
from pydantic.color import Color
from sqlmodel import Relationship, SQLModel, Field, Column
from .multiscale.cosem import SpatialTransform
from sqlalchemy.dialects import postgresql
from typing import Any

class MeshTypeEnum(str, Enum):
    """
    Strings representing supported mesh formats
    """

    neuroglancer_legacy_mesh = "neuroglancer_legacy_mesh"
    neuroglancer_multilod_draco = "neuroglancer_multilod_draco"


class ArrayContainerTypeEnum(str, Enum):
    n5 = "n5"
    zarr = "zarr"
    precomputed = "precomputed"


class ContentTypeEnum(str, Enum):
    em = "em"
    lm = "lm"
    prediction = "prediction"
    segmentation = "segmentation"
    analysis = "analysis"


class SampleTypeEnum(str, Enum):
    scalar = "scalar"
    label = "label"


class ContrastLimits(SQLModel):
    start: int
    end: int
    min: int
    max: int


class DisplaySettingsBase(SQLModel):
    """
    Metadata for display settings
    """

    contrastLimits: ContrastLimits
    color: Color | None
    invertLUT: bool


class DisplaySettings(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    contrastLimits: dict[Any, Any] = Field(sa_column=Column(postgresql.JSONB))

class DataSource(SQLModel):
    """
    An abstract data source. Volume and mesh source metadata are
    derived from this interface.
    """
    name: str
    description: str
    url: str
    format: str
    transform: SpatialTransform


class MeshBase(DataSource):
    format: MeshTypeEnum
    ids: list[int]


class Mesh(MeshBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transform: dict[Any, Any] = Field(sa_column=Column(postgresql.JSONB))

class VolumeBase(DataSource):
    format: ArrayContainerTypeEnum
    sampleType: SampleTypeEnum
    contentType: ContentTypeEnum
    displaySettings: DisplaySettings
    #subsources: list[Mesh]


class Volume(VolumeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    displaySettings_id: int | None = Field(foreign_key='displaysettings.id')
    displaySettings: DisplaySettings = Relationship()
    transform: dict[Any, Any] = Field(sa_column=Column(postgresql.JSONB))