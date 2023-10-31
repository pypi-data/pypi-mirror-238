from copy import deepcopy
from typing import List, Optional, Iterable, Iterator, Sized, Union

from auto_phylo.pipeliner.model.Command import Command
from auto_phylo.pipeliner.model.PipelineChangeEvent import PipelineChangeEvent
from auto_phylo.pipeliner.model.PipelineChangeType import PipelineChangeType
from auto_phylo.pipeliner.util.Observable import Observable


class PipelineIterator(Iterator[Command]):
    def __init__(self, pipeline: "Pipeline"):
        self._pipeline: Pipeline = pipeline
        self._index: int = 0

    def __next__(self) -> Command:
        if self._index == len(self._pipeline.commands):
            raise StopIteration
        else:
            item = self._pipeline.commands[self._index]
            self._index += 1

            return item


class Pipeline(Observable, Iterable[Command], Sized):
    def __init__(self, commands: Optional[List[Command]] = None):
        super().__init__()
        self._commands: List[Command] = [] if commands is None else commands.copy()

    @property
    def commands(self) -> List[Command]:
        return self._commands.copy()

    def is_valid(self) -> bool:
        return len(self._commands) > 0

    def has_command(self, target_command: Union[Command, str]) -> bool:
        target_command = target_command if isinstance(target_command, str) else target_command.tool

        return any(command for command in self._commands if command.tool == target_command)

    def add_command(self, command: Command) -> int:
        self._commands.append(command)

        index = len(self._commands) - 1

        self._notify_observers(PipelineChangeEvent(PipelineChangeType.ADD, index))

        return index

    def insert_command(self, index: int, command: Command) -> None:
        self._commands.insert(index, command)

        self._notify_observers(PipelineChangeEvent(PipelineChangeType.INSERT, index))

    def remove_command(self, index: int) -> None:
        self._commands.pop(index)
        self._notify_observers(PipelineChangeEvent(PipelineChangeType.REMOVE, index))

    def remove_all_instances_of_command(self, command: Command) -> None:
        indexes = self.get_command_indexes(command)
        indexes.reverse()

        for index in indexes:
            self.remove_command(index)

    def swap_command_position(self, index_a: int, index_b: int) -> None:
        self._commands[index_a], self._commands[index_b] = self._commands[index_b], self._commands[index_a]
        self._notify_observers(PipelineChangeEvent(PipelineChangeType.SWAP, index_a, index_b))

    def get_command_indexes(self, command: Command) -> List[int]:
        return [index for index, value in enumerate(self._commands) if value == command]

    def find_command_with_param(self, param: str) -> Command:
        try:
            return next(command for command in self._commands if command.has_param(param))
        except StopIteration:
            raise ValueError(f"Unknown parameter {param}")

    def clear(self) -> None:
        last_index = len(self._commands) - 1
        self._commands.clear()
        self._notify_observers(PipelineChangeEvent(PipelineChangeType.CLEAR, 0, last_index))

    def __len__(self) -> int:
        return len(self._commands)

    def __iter__(self) -> Iterator[Command]:
        return PipelineIterator(self)

    def __copy__(self) -> "Pipeline":
        return Pipeline(self._commands)

    def __deepcopy__(self, memodict={}) -> "Pipeline":
        return Pipeline(deepcopy(self._commands))
