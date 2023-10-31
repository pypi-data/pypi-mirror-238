from typing import Optional

from auto_phylo.pipeliner.model.PipelineChangeType import PipelineChangeType


class PipelineChangeEvent:
    def __init__(self, action: PipelineChangeType, index_a: int, index_b: Optional[int] = None):
        self._action: PipelineChangeType = action
        self._index_a: int = index_a
        self._index_b: Optional[int] = index_b

    @property
    def action(self) -> PipelineChangeType:
        return self._action

    @property
    def index(self) -> int:
        return self._index_a

    @property
    def index_a(self) -> int:
        return self._index_a

    @property
    def index_b(self) -> Optional[int]:
        return self._index_b

    def __str__(self):
        return (f"{self.__class__.__name__}[action: {self._action}, "
                f"index_a: {self._index_a}, index_b: {self._index_b}]")
