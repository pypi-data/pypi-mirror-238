from enum import auto, Enum


class PipelineChangeType(Enum):
    ADD = auto()
    INSERT = auto()
    REMOVE = auto()
    SWAP = auto()
    CLEAR = auto()
