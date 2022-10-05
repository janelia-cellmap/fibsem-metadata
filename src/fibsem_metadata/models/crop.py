from enum import Enum
from typing import List

from .base import Base
from .multiscale.cosem import SpatialTransform
from .source import Image


class CompletionStage(str, Enum):
    validation = "Validation"
    training_active = "In training"
    training_ready = "Ready for training"
    convert_h5 = "Converted to h5"
    finalization = "Finalization and export"
    annotation_detailed = "Detailed annotation"
    annotation_bulk = "Bulk annotation"


class LabelName(Base):
    long: str
    short: str


LABELS = (
    LabelName(long="Centrosome", short="Centrosome"),
    LabelName(long="Centrosome Distal Appendage", short="Controsome D App"),
    LabelName(long="Centrosome Subdistal Appendage", short="Controsome SD App"),
    LabelName(long="Chromatin", short="Chromatin"),
    LabelName(long="Extracellular Space", short="ECS"),
    LabelName(long="Endosomal Network", short="Endo"),
    LabelName(long="Endosome Membrane", short="Endo mem"),
    LabelName(long="Endoplasmic Reticulum", short="ER"),
    LabelName(long="Endoplasmic Reticulum Membrane", short="ER mem"),
    LabelName(long="Endoplasmic Reticulum Exit Site", short="ERES"),
    LabelName(long="Endoplasmic Reticulum Exit Site Membrane", short="ERES mem"),
    LabelName(long="Euchromatin", short="E Chrom"),
    LabelName(long="Nucleolus-associated Euchromatin", short="N-E Chrom"),
    LabelName(long="Golgi", short="Golgi"),
    LabelName(long="Golgi Membrane", short="Golgi Mem"),
    LabelName(long="Heterochromatin", short="H Chrom"),
    LabelName(long="Nucleolus-associated Heterochromatin", short="N-H Chrom"),
    LabelName(long="Lipid Droplet", short="LD"),
    LabelName(long="Lipid Droplet Membrane", short="LD mem"),
    LabelName(long="Lysosome", short="Lyso"),
    LabelName(long="Lysosome membrane", short="Lyso mem"),
    LabelName(long="Microtubule", short="MT"),
    LabelName(long="Microtubule outer", short="MT out"),
    LabelName(long="Mitochondria", short="Mito"),
    LabelName(long="Mitochondria Membrane", short="Mito mem"),
    LabelName(long="Mitochondria Ribosome", short="Mito Ribo"),
    LabelName(long="Nuclear Envelope", short="NE"),
    LabelName(long="Nuclear Envelope", short="NE mem"),
    LabelName(long="Nuclear Pore", short="NP"),
    LabelName(long="Nuclear Pore outer", short="NP out"),
    LabelName(long="Plasma Membrane", short="PM"),
    LabelName(long="Nucleolus", short="Nucleolus"),
    LabelName(long="Nucleus", short="Nucleus"),
    LabelName(long="Ribosome", short="Ribo"),
    LabelName(long="Vesicle", short="Vesicle"),
    LabelName(long="Vesicle membrane", short="Vesicle mem"),
)


class AnnotationState(Base):
    present: bool
    annotated: bool


class Label(Base):
    name: LabelName
    value: int
    annotation_state: AnnotationState


class Crop(Base):
    name: str
    description: str
    source: Image
    annotations: List[Label]
    shape: List[int]
    completion_stage: CompletionStage
    transform_world: SpatialTransform
    transform_source: SpatialTransform
