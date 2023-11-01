from copy import deepcopy
from typing import List, Optional, Union, Dict

from auto_phylo.pipeliner.model.Command import Command
from auto_phylo.pipeliner.model.CommandConfiguration import CommandConfiguration
from auto_phylo.pipeliner.model.CommandConfigurationEvent import CommandConfigurationEvent
from auto_phylo.pipeliner.model.Pipeline import Pipeline
from auto_phylo.pipeliner.model.PipelineChangeEvent import PipelineChangeEvent
from auto_phylo.pipeliner.model.PipelineChangeType import PipelineChangeType
from auto_phylo.pipeliner.model.PipelineConfigurationChangeEvent import PipelineConfigurationChangeEvent
from auto_phylo.pipeliner.util.Observable import Observable


class PipelineConfiguration(Observable):
    def __init__(self,
                 pipeline: Pipeline,
                 seda_version: Optional[str] = None,
                 output_dir: Optional[str] = None,
                 command_configs: Optional[List[CommandConfiguration]] = None):
        super().__init__()

        self._pipeline: Pipeline = pipeline
        self._seda_version: Optional[str] = seda_version
        self._output_dir: Optional[str] = output_dir

        self._command_configs: List[CommandConfiguration]
        if command_configs is None:
            self._command_configs = [CommandConfiguration(command) for command in pipeline]
        else:
            if len(pipeline) != len(command_configs):
                raise ValueError("pipeline and command_configs must have the same length")

            for command, command_config in zip(pipeline, command_configs):
                if command_config is None or command.tool != command_config.command.tool:
                    raise ValueError("pipeline and command_configs commands do not match")

            self._command_configs = command_configs.copy()

        self._pipeline.add_callback(self._on_pipeline_change)
        for command_config in self._command_configs:
            command_config.add_callback(self._on_command_config_change)

    @property
    def pipeline(self) -> Pipeline:
        return self._pipeline

    @property
    def seda_version(self) -> Optional[str]:
        return self._seda_version

    @seda_version.setter
    def seda_version(self, seda_version: Optional[str]) -> None:
        if seda_version is not None:
            seda_version = seda_version.strip()

            if len(seda_version) == 0:
                seda_version = None

        if self._seda_version != seda_version:
            old_value = self._seda_version

            self._seda_version = seda_version

            self._notify_observers(PipelineConfigurationChangeEvent("seda_version", old_value, self._seda_version))

    @property
    def output_dir(self) -> Optional[str]:
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir: Optional[str]) -> None:
        if output_dir is not None:
            output_dir = output_dir.strip()

            if len(output_dir) == 0:
                output_dir = None

        if self._output_dir != output_dir:
            old_value = self._output_dir

            self._output_dir = output_dir

            self._notify_observers(PipelineConfigurationChangeEvent("output_dir", old_value, self._output_dir))

    @property
    def command_configs(self) -> List[CommandConfiguration]:
        return self._command_configs.copy()

    def is_valid_pipeline(self) -> bool:
        return self._output_dir is not None \
            and self._pipeline.is_valid() \
            and all(command_config.is_valid_pipeline() for command_config in self._command_configs)

    def is_valid_config(self) -> bool:
        return self._seda_version is not None \
            and self._output_dir is not None \
            and all(command_config.is_valid_config() for command_config in self._command_configs)

    def set_command_param_value(self, command: Union[Command, str], param: str, new_value: str) -> None:
        tool = command if isinstance(command, str) else command.tool

        found = False
        for command_config in self._command_configs:
            if command_config.command.tool == tool:
                command_config.set_param_value(param, new_value)

                found = True

        if not found:
            raise ValueError(f"Unknown command {tool}")

    def get_command_param_value(self, command: Union[Command, str], param: str) -> str:
        tool = command if isinstance(command, str) else command.tool

        for command_config in self._command_configs:
            if command_config.command.tool == tool:
                return command_config.get_param_value(param)

        raise ValueError(f"Unknown command {tool}")

    def get_command_param_values(self, command: Union[Command, str]) -> Dict[str, str]:
        tool = command if isinstance(command, str) else command.tool

        for command_config in self._command_configs:
            if command_config.command.tool == tool:
                return command_config.param_values

        raise ValueError(f"Unknown command {tool}")

    def list_command_param_names(self, command: Command) -> List[str]:
        tool = command if isinstance(command, str) else command.tool

        for command_config in self._command_configs:
            if command_config.command.tool == tool:
                return command_config.list_param_names()

        raise ValueError(f"Unknown command {tool}")

    def get_command_configuration(self, index: int) -> CommandConfiguration:
        return self._command_configs[index]

    def set_command_configuration(self, index: int, command_config: CommandConfiguration) -> None:
        pipeline_command_tool = self._pipeline.commands[index].tool
        config_command_tool = command_config.command.tool

        if pipeline_command_tool != config_command_tool:
            raise ValueError(
                f"Config command {config_command_tool} does not match pipeline command {pipeline_command_tool}")

        command_config.copy_to(self._command_configs[index])

        for i, cc in enumerate(self._command_configs):
            if i != index and cc.command.tool == command_config.command.tool:
                cc.set_param_values(command_config.param_values)

    def replace_command_configuration(self, index: int, command_config: CommandConfiguration) -> None:
        if index < 0 or index > len(self._pipeline) - 1:
            raise IndexError("Index out of bounds")

        self._pipeline.remove_command(index)
        self._pipeline.insert_command(index, command_config.command)
        self.set_command_configuration(index, command_config)

    def _on_pipeline_change(self, pipeline: Pipeline, event: PipelineChangeEvent) -> None:
        index = event.index

        if event.action == PipelineChangeType.ADD or event.action == PipelineChangeType.INSERT:
            command = pipeline.commands[index]
            new_config = CommandConfiguration(command)

            self._command_configs.insert(index, new_config)
            new_config.add_callback(self._on_command_config_change)

            self._notify_observers(PipelineConfigurationChangeEvent("command_configs", None, (index, new_config)))
        elif event.action == PipelineChangeType.REMOVE:
            old_config = self._command_configs.pop(index)

            self._notify_observers(PipelineConfigurationChangeEvent("command_configs", (index, old_config), None))
        elif event.action == PipelineChangeType.SWAP:
            config_a = self._command_configs[event.index_a]
            config_b = self._command_configs[event.index_b]  # type: ignore

            self._command_configs[event.index_a], self._command_configs[event.index_b] = (  # type: ignore
                config_b, config_a)

            self._notify_observers(PipelineConfigurationChangeEvent("command_configs", (event.index_a, config_a),
                                                                    (event.index_b, config_a)))
            self._notify_observers(PipelineConfigurationChangeEvent("command_configs", (event.index_b, config_b),
                                                                    (event.index_a, config_b)))
        elif event.action == PipelineChangeType.CLEAR:
            command_configs = self._command_configs.copy()
            self._command_configs.clear()
            self._notify_observers(PipelineConfigurationChangeEvent("command_configs", command_configs, None))

    def _on_command_config_change(self, command_config: CommandConfiguration, _: CommandConfigurationEvent) -> None:
        if command_config in self._command_configs:
            index = self._command_configs.index(command_config)

            self._notify_observers(
                PipelineConfigurationChangeEvent("command_configs", (index, command_config), (index, command_config)))

    def __copy__(self) -> "PipelineConfiguration":
        return PipelineConfiguration(
            self._pipeline,
            self._seda_version,
            self._output_dir,
            self._command_configs
        )

    def __deepcopy__(self, memodict={}) -> "PipelineConfiguration":
        return PipelineConfiguration(
            deepcopy(self._pipeline),
            self._seda_version,
            self._output_dir,
            deepcopy(self._command_configs)
        )
