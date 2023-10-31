from auto_phylo.pipeliner.model.CommandConfiguration import CommandConfiguration as CommandConfiguration
from auto_phylo.pipeliner.model.CommandConfigurationEvent import CommandConfigurationEvent as CommandConfigurationEvent
from tkinter import Misc, Toplevel
from typing import Optional

class ParamConfigurationDialog(Toplevel):
    def __init__(self, command_config: CommandConfiguration, master: Optional[Misc] = ...) -> None: ...
