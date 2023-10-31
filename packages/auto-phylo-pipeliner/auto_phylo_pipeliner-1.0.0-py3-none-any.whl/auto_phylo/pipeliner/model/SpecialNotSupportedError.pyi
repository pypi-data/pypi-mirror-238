from auto_phylo.pipeliner.model.Command import Command as Command
from builtins import Exception

class SpecialNotSupportedError(Exception):
    def __init__(self, command: Command) -> None: ...
    @property
    def command(self): ...
