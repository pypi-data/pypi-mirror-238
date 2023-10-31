from builtins import Exception

from auto_phylo.pipeliner.model.Command import Command


class SpecialNotSupportedError(Exception):
    def __init__(self, command: Command):
        super().__init__(f"Command '{command.name}' does not support special")
        self._command: Command = command

    @property
    def command(self):
        return self._command
