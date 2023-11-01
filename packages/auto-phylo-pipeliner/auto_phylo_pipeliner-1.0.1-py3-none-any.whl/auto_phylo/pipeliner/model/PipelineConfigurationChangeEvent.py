from typing import Any, Optional


class PipelineConfigurationChangeEvent:
    def __init__(self, attribute: str, old_value: Optional[Any], new_value: Optional[Any]):
        self._attribute: str = attribute
        self._old_value: Optional[Any] = old_value
        self._new_value: Optional[Any] = new_value

    @property
    def attribute(self) -> str:
        return self._attribute

    @property
    def old_value(self) -> Optional[Any]:
        return self._old_value

    @property
    def new_value(self) -> Optional[Any]:
        return self._new_value

    def __str__(self) -> str:
        return (f"PipelineConfigurationChangeEvent[attribute={self._attribute}, old_value={self._old_value}, "
                f"new_value={self._new_value}]")
