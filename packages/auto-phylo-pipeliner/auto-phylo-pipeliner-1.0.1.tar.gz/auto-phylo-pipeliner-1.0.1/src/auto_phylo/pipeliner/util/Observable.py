from typing import List, Callable, TypeVar, Generic

E = TypeVar("E")

Self = TypeVar("Self", bound="Observable")


class Observable(Generic[E]):
    def __init__(self):
        self._callbacks: List[Callable[[Self, E], None]] = []

    def _notify_observers(self, event: E) -> None:
        for callback in self._callbacks:
            callback(self, event)

    def add_callback(self, callback: Callable[[Self, E], None]) -> None:
        self._callbacks = self._callbacks.copy()
        self._callbacks.append(callback)  # type: ignore

    def has_callback(self, callback: Callable[[Self, E], None]) -> bool:
        return callback in self._callbacks

    def remove_callback(self, callback: Callable[[Self, E], None]) -> None:
        self._callbacks = self._callbacks.copy()
        self._callbacks.remove(callback)  # type: ignore

    def remove_all_callbacks(self) -> None:
        self._callbacks = self._callbacks.copy()
        self._callbacks.clear()
