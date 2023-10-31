from tkinter import Toplevel, Misc, Entry, StringVar
from tkinter.ttk import Button, Label, Style
from typing import Optional, Final, Tuple, Dict

from auto_phylo.pipeliner.model.CommandConfiguration import CommandConfiguration
from auto_phylo.pipeliner.model.CommandConfigurationEvent import CommandConfigurationEvent


class ParamConfigurationDialog(Toplevel):
    _COLOR_ERROR: Final[str] = "#ff4444"
    _STYLE_ERROR_LABEL: Final[str] = "ParamConfigurationDialog_Error.TLabel"

    def __init__(self, command_config: CommandConfiguration, master: Optional[Misc] = None):
        super().__init__(master)

        self._command_config: CommandConfiguration = command_config
        self._param_fields: Dict[str, Tuple[Label, Entry, StringVar]] = {}

        self.title(f"Configure {command_config.command.name}")

        style = Style()
        style.configure(ParamConfigurationDialog._STYLE_ERROR_LABEL,
                        foreground=ParamConfigurationDialog._COLOR_ERROR)

        row = 0
        for param in command_config.command.list_param_names():
            label = Label(self, text=param)

            sv_entry = StringVar(self)
            if command_config.has_param_value(param):
                sv_entry.set(command_config.get_param_value(param))

            entry = Entry(self, textvariable=sv_entry)
            self._bind_value_change(param, entry)

            label.grid(row=row, column=0, sticky="nsew", padx=5, pady=2)
            entry.grid(row=row, column=1, sticky="nsew", padx=5, pady=2)

            self._param_fields[param] = (label, entry, sv_entry)

            row += 1

        self._btn_exit: Button = Button(self, text="Close", command=self._on_close)
        self._btn_exit.grid(row=row, column=0, columnspan=2, padx=4, pady=4)

        self._update_param_labels()

        self._command_config.add_callback(self._on_command_config_change)

    def _bind_value_change(self, param: str, entry: Entry) -> None:
        entry.bind("<FocusOut>", lambda event: self._command_config.set_param_value(param, event.widget.get()))

    def _on_command_config_change(self, _: CommandConfiguration, event: CommandConfigurationEvent) -> None:
        if event.attribute.startswith("param_values"):
            self._update_param_labels()

    def _on_close(self) -> None:
        self._command_config.remove_callback(self._on_command_config_change)
        self.destroy()

    def _update_param_labels(self):
        for param in self._command_config.list_param_names():
            label = self._param_fields[param][0]

            if self._command_config.has_valid_param_value(param):
                label.configure(style="TLabel")
            else:
                label.configure(style=ParamConfigurationDialog._STYLE_ERROR_LABEL)
