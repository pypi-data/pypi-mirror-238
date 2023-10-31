from copy import deepcopy
from typing import Optional, Dict, List

from auto_phylo.pipeliner.model.Command import Command
from auto_phylo.pipeliner.model.CommandConfigurationEvent import CommandConfigurationEvent
from auto_phylo.pipeliner.model.SpecialNotSupportedError import SpecialNotSupportedError
from auto_phylo.pipeliner.util.Observable import Observable


class CommandConfiguration(Observable[CommandConfigurationEvent]):
    def __init__(self, command: Command,
                 input_dir: Optional[str] = None,
                 output_dir: Optional[str] = None,
                 special: Optional[int] = None,
                 param_values: Optional[Dict[str, str]] = None):
        super().__init__()
        self._command: Command = command
        self._input_dir: Optional[str] = input_dir
        self._output_dir: Optional[str] = output_dir
        self._special: Optional[int] = special
        self._param_values: Dict[str, str]

        if param_values is None:
            self._param_values = command.params
        else:
            self._param_values = {}

            self._replace_param_values(param_values)

    @property
    def command(self) -> Command:
        return self._command

    @property
    def input_dir(self) -> Optional[str]:
        return self._input_dir

    @input_dir.setter
    def input_dir(self, input_dir: Optional[str]) -> None:
        if input_dir is not None:
            input_dir = input_dir.strip()

            if len(input_dir) == 0:
                input_dir = None

        if self._input_dir != input_dir:
            old_value = self._input_dir

            self._input_dir = input_dir

            self._notify_observers(CommandConfigurationEvent("input_dir", old_value, self._input_dir))

    def has_input_dir(self) -> bool:
        return self._input_dir is not None

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

            self._notify_observers(CommandConfigurationEvent("output_dir", old_value, self._output_dir))

    def has_output_dir(self) -> bool:
        return self._output_dir is not None

    @property
    def special(self) -> Optional[int]:
        if not self.command.supports_special:
            raise SpecialNotSupportedError(self._command)

        return self._special

    @special.setter
    def special(self, special: Optional[int]) -> None:
        if not self.command.supports_special:
            raise SpecialNotSupportedError(self._command)

        if special is not None and special < 1:
            raise ValueError("special must be None or positive")

        if self._special != special:
            old_value = self._special

            self._special = special

            self._notify_observers(CommandConfigurationEvent("special", old_value, self._special))

    def is_valid_pipeline(self) -> bool:
        return self._input_dir is not None \
            and self._output_dir is not None

    def is_valid_config(self) -> bool:
        return all(self.has_param_value(param) or self.command.does_param_allow_empty(param)
                    for param in self.command.params)

    def is_special_supported(self) -> bool:
        return self._command.supports_special

    def has_special(self) -> bool:
        return self._special is not None

    def remove_special(self) -> None:
        if not self.command.supports_special:
            raise SpecialNotSupportedError(self._command)

        self._special = None

    @property
    def param_values(self) -> Dict[str, str]:
        return self._param_values.copy()

    def has_param(self, param: str) -> bool:
        return self._command.has_param(param)

    def list_param_names(self) -> List[str]:
        return self._command.list_param_names()

    def has_param_value(self, param: str) -> bool:
        return self._param_values[param] != ""

    def has_valid_param_value(self, param: str) -> bool:
        return self._param_values[param] != "" or self._command.does_param_allow_empty(param)

    def get_param_value(self, param: str) -> str:
        return self._param_values[param]

    def set_param_value(self, param: str, new_value: str) -> None:
        if not self._command.has_param(param):
            raise ValueError(f"{param} is not a valid param")

        new_value = new_value.strip()
        if param not in self._param_values or self._param_values[param] != new_value:
            old_value = self._param_values[param] if param in self._param_values else None

            self._param_values[param] = new_value

            self._notify_observers(CommandConfigurationEvent(f"param_values[{param}]", old_value, new_value))

    def remove_param_value(self, param: str) -> None:
        if not self._command.has_param(param):
            raise ValueError(f"{param} is not a valid param")

        if param not in self._param_values:
            raise ValueError(f"{param} does not have a value")

        old_value = self._param_values[param]

        self._param_values[param] = ""

        self._notify_observers(CommandConfigurationEvent(f"param_values[{param}]", old_value, ""))

    def set_param_values(self, params: Dict[str, str]) -> None:
        old_value = self._param_values

        self._replace_param_values(params)

        self._notify_observers(CommandConfigurationEvent(f"param_values", old_value, params))

    def clear_param_values(self) -> None:
        old_value = self._param_values

        self._param_values.clear()

        self._notify_observers(CommandConfigurationEvent(f"param_values", old_value, None))

    def has_param_values(self):
        return len(self._param_values) > 0

    def copy_to(self, command_config: "CommandConfiguration") -> None:
        command_config.input_dir = self._input_dir
        command_config.output_dir = self._output_dir

        if command_config.is_special_supported() and self.has_special():
            command_config.special = self._special

        if command_config.command.tool == self._command.tool:
            command_config.set_param_values(self._param_values)

    def _replace_param_values(self, param_values: Dict[str, str]) -> None:
        param_names = self._command.list_param_names()
        for param, value in param_values.items():
            if param not in param_names:
                raise ValueError(f"Param {param} does not belong to the command {self._command.name}")

        self._param_values.clear()
        self._param_values = param_values.copy()

        for param in param_names:
            if param not in self._param_values:
                self._param_values[param] = ""

    def __copy__(self) -> "CommandConfiguration":
        return CommandConfiguration(
            self._command,
            self._input_dir,
            self._output_dir,
            self._special,
            self._param_values
        )

    def __deepcopy__(self, memodict={}) -> "CommandConfiguration":
        return CommandConfiguration(
            self._command,
            self._input_dir,
            self._output_dir,
            self._special,
            deepcopy(self._param_values)
        )
