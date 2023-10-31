from auto_phylo.pipeliner.model.CommandConfiguration import CommandConfiguration as CommandConfiguration
from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration as PipelineConfiguration
from typing import TextIO

class ConfigurationParser:
    def parse(self, text: TextIO, pipeline_configuration: PipelineConfiguration) -> PipelineConfiguration: ...
