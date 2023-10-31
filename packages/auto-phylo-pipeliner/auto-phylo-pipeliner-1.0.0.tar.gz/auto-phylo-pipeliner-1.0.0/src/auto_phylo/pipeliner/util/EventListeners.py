from typing import Generic, TypeVar, Callable, List, Optional

E = TypeVar("E")


class EventQueue(Generic[E]):
    def __init__(self):
        self._callback: Optional[Callable[[E], None]] = None

    def register_callback(self, callback: Callable[[E], None]):
        self._callback = callback

    def notify(self, event: E):
        if self._callback is not None:
            self._callback(event)


class EventListeners(Generic[E]):
    def __init__(self, queue: EventQueue[E]):
        self._callbacks: List[Callable[[E], None]] = []

        queue.register_callback(self._notify)

    def _notify(self, event: E):
        for callback in self._callbacks:
            callback(event)

    def add_callback(self, callback: Callable[[E], None]) -> None:
        self._callbacks = self._callbacks.copy()

        self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[E], None]) -> None:
        if self.has_callback(callback):
            self._callbacks = self._callbacks.copy()
            self._callbacks.remove(callback)
        else:
            raise ValueError("callback is not registered")

    def has_callback(self, callback: Callable[[E], None]) -> bool:
        return callback in self._callbacks

    def clear_callbacks(self) -> None:
        self._callbacks = []
