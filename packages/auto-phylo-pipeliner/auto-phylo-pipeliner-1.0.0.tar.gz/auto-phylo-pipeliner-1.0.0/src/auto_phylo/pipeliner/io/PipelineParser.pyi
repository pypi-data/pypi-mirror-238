from auto_phylo.pipeliner.model.Commands import Commands as Commands
from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration
from typing import TextIO

class PipelineParser:
    def __init__(self, commands: Commands = ...) -> None: ...
    def parse(self, text: TextIO) -> PipelineConfiguration: ...
