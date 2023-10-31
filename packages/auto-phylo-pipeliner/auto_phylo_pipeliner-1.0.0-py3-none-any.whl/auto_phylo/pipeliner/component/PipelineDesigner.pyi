from auto_phylo.pipeliner.model.Command import Command as Command
from auto_phylo.pipeliner.model.CommandConfigurationEvent import CommandConfigurationEvent as CommandConfigurationEvent
from auto_phylo.pipeliner.model.Commands import Commands as Commands
from auto_phylo.pipeliner.model.Pipeline import Pipeline as Pipeline
from auto_phylo.pipeliner.model.PipelineChangeEvent import PipelineChangeEvent as PipelineChangeEvent
from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration as PipelineConfiguration
from auto_phylo.pipeliner.model.PipelineConfigurationChangeEvent import PipelineConfigurationChangeEvent as PipelineConfigurationChangeEvent
from tkinter import Widget
from tkinter.ttk import Frame
from typing import Optional

class PipelineDesigner(Frame):
    def __init__(self, pipeline_configuration: PipelineConfiguration, commands: Commands = ..., master: Optional[Widget] = ..., *args, **kwargs) -> None: ...
    @property
    def pipeline_configuration(self) -> PipelineConfiguration: ...
    def configure(self, **kwargs) -> None: ...

class _CommandConfigFormMediator:
    def __init__(self, master: Frame, index: int, pipeline_configuration: PipelineConfiguration, commands: Commands, **kwargs) -> None: ...
    def destroy(self) -> None: ...
