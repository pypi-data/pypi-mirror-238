from typing import Any


class CommandConfigurationEvent:
    def __init__(self, attribute: str, old_value: Any, new_value: Any):
        self._attribute: str = attribute
        self._old_value: Any = old_value
        self._new_value: Any = new_value

    @property
    def attribute(self) -> str:
        return self._attribute

    @property
    def old_value(self) -> Any:
        return self._old_value

    @property
    def new_value(self) -> Any:
        return self._new_value

    def __str__(self):
        return (f"{self.__class__.__name__}[attribute: {self._attribute}, "
                f"old_value: {self._old_value}, new_value: {self._new_value}]")
