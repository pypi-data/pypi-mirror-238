import webbrowser
from tkinter import Widget, StringVar, Event, BooleanVar
from tkinter.constants import NORMAL, DISABLED
from tkinter.font import Font
from tkinter.ttk import Frame, OptionMenu, Entry, Spinbox, Button, Checkbutton, Style, Label
from typing import Optional, Dict, Any, List, Final, Tuple
import os
import sys

from auto_phylo.pipeliner import load_commands
from auto_phylo.pipeliner.component.ParamConfigurationDialog import ParamConfigurationDialog
from auto_phylo.pipeliner.model.Command import Command
from auto_phylo.pipeliner.model.CommandConfiguration import CommandConfiguration
from auto_phylo.pipeliner.model.CommandConfigurationEvent import CommandConfigurationEvent
from auto_phylo.pipeliner.model.Commands import Commands
from auto_phylo.pipeliner.model.Pipeline import Pipeline
from auto_phylo.pipeliner.model.PipelineChangeEvent import PipelineChangeEvent
from auto_phylo.pipeliner.model.PipelineChangeType import PipelineChangeType
from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration
from auto_phylo.pipeliner.model.PipelineConfigurationChangeEvent import PipelineConfigurationChangeEvent


class PipelineDesigner(Frame):
    _PAD_X: Final[Tuple[int, int]] = (4, 4)
    _PAD_Y: Final[Tuple[int, int]] = (2, 2)

    def __init__(self, pipeline_configuration: PipelineConfiguration, commands: Commands = load_commands(),
                 master: Optional[Widget] = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._commands: Commands = commands
        self._pipeline_configuration: PipelineConfiguration = pipeline_configuration

        self._mediators: List[_CommandConfigFormMediator] = []
        self._btn_new: Button = Button(self, text="Add command", command=self._on_add_command)

        self._rebuild_form()
        self._pipeline_configuration.add_callback(self._on_pipeline_config_change)

    @property
    def pipeline_configuration(self) -> PipelineConfiguration:
        return self._pipeline_configuration

    @pipeline_configuration.setter
    def pipeline_configuration(self, pipeline_config: PipelineConfiguration) -> None:
        if self._pipeline_configuration != pipeline_config:
            self._pipeline_configuration.remove_callback(self._on_pipeline_config_change)

            self._rebuild_form()

            self._pipeline_configuration.add_callback(self._on_pipeline_config_change)

    def configure(self, **kwargs):
        if "state" in kwargs:
            self._change_children_state(kwargs.pop("state"))
        if kwargs:
            super().configure(**kwargs)

    def _rebuild_form(self):
        for mediator in self._mediators:
            mediator.destroy()

        self._mediators.clear()

        for index in range(0, len(self._pipeline_configuration.pipeline)):
            self._mediators.append(_CommandConfigFormMediator(self, index, self._pipeline_configuration, self._commands,
                                                              padx=PipelineDesigner._PAD_X,
                                                              pady=PipelineDesigner._PAD_Y))
        self._btn_new.grid(row=len(self._mediators), column=0, columnspan=13, padx=PipelineDesigner._PAD_X,
                           pady=PipelineDesigner._PAD_Y)

    def _change_children_state(self, state: str) -> None:
        for child in self.winfo_children():
            child.configure(state=state)  # type: ignore

    def _get_first_unselected_command(self) -> Command:
        for command in self._commands:
            if not self._pipeline_configuration.pipeline.has_command(command):
                return command

        return self._commands.commands[0]

    def _add_command_config_form(self, index: int) -> None:
        self._mediators.append(_CommandConfigFormMediator(self, index, self._pipeline_configuration, self._commands,
                                                          padx=PipelineDesigner._PAD_X,
                                                          pady=PipelineDesigner._PAD_Y))
        self._btn_new.grid(row=len(self._mediators), column=0, columnspan=10,
                           padx=PipelineDesigner._PAD_X, pady=PipelineDesigner._PAD_Y)

    def _on_pipeline_config_change(self, _: PipelineConfiguration, event: PipelineConfigurationChangeEvent) -> None:
        if event.attribute == "command_configs" and event.old_value is None:
            index = event.new_value[0]  # type: ignore

            self._add_command_config_form(index)

    def _on_add_command(self) -> None:
        index = self._pipeline_configuration.pipeline.add_command(self._get_first_unselected_command())

        self._add_command_config_form(index)


class _CommandConfigFormMediator:
    _COLOR_ERROR: Final[str] = "#ff4444"
    _STYLE_ERROR_LABEL: Final[str] = "PipelineDesigner_CommandConfigFormMediator_Error.TLabel"

    def __init__(self, master: Frame,
                 index: int,
                 pipeline_configuration: PipelineConfiguration,
                 commands: Commands,
                 **kwargs):
        self._master: Frame = master
        self._index: int = index
        self._command_config: CommandConfiguration = pipeline_configuration.get_command_configuration(index)
        self._pipeline_configuration: PipelineConfiguration = pipeline_configuration
        self._commands: Commands = commands
        self._grid_kwargs: Dict[str, Any] = kwargs

        self._btn_up = Button(master, text="↑", width=2)
        self._btn_down = Button(master, text="↓", width=2)

        command_names = commands.list_names()
        self._sv_om_commands = StringVar(master)
        self._om_commands = OptionMenu(master, self._sv_om_commands, command_names[0], *command_names)
        self._om_commands.configure(width=25)

        style = Style()
        style.configure(_CommandConfigFormMediator._STYLE_ERROR_LABEL,
                        foreground=_CommandConfigFormMediator._COLOR_ERROR,
                        font=Font(family="TkFixedFont", weight="bold"))

        self._sv_lbl_input = StringVar()
        self._e_input = Entry(master, width=10)
        self._lbl_input = Label(master, textvariable=self._sv_lbl_input)
        self._lbl_input.configure(style=_CommandConfigFormMediator._STYLE_ERROR_LABEL)

        self._sv_lbl_output = StringVar()
        self._e_output = Entry(master, width=10)
        self._lbl_output = Label(master, textvariable=self._sv_lbl_output)
        self._lbl_output.configure(style=_CommandConfigFormMediator._STYLE_ERROR_LABEL)

        self._bv_chk_special = BooleanVar(master)
        self._chk_special = Checkbutton(master, text="Special", variable=self._bv_chk_special)
        self._sb_special = Spinbox(master, from_=1, to=100, increment=1, width=3)

        self._btn_params = Button(master, text="Params")
        self._btn_info = Button(master, text="Info")
        self._btn_remove = Button(master, text="X", width=2)

        self._sv_lbl_params = StringVar()
        self._lbl_params = Label(master, textvariable=self._sv_lbl_params)
        self._lbl_params.configure(style=_CommandConfigFormMediator._STYLE_ERROR_LABEL)

        self._update_position()
        self._update_command()
        self._update_input_dir()
        self._update_output_dir()
        self._update_special()
        self._update_params()

        self._e_input.bind("<FocusOut>", self._on_input_change)
        self._e_output.bind("<FocusOut>", self._on_output_change)

        self._sv_om_commands.trace_add("write", self._on_command_change)
        self._chk_special.configure(command=self._on_special_activation_change)
        self._sb_special.configure(command=self._on_special_change)
        self._sb_special.bind("<FocusOut>", self._on_special_change)

        self._btn_down.configure(command=self._on_down_command)
        self._btn_up.configure(command=self._on_up_command)
        self._btn_params.configure(command=self._on_params_command)
        self._btn_info.configure(command=self._on_info_command)
        self._btn_remove.configure(command=self._on_remove_command)

        self._command_config.add_callback(self._on_command_config_change)
        self._pipeline_configuration.pipeline.add_callback(self._on_pipeline_change)

    def _locate_components(self) -> None:
        lbl_kwargs = self._grid_kwargs.copy()
        pre_lbl_kwargs = self._grid_kwargs.copy()

        if "padx" in self._grid_kwargs:
            pre_lbl_kwargs["padx"] = (pre_lbl_kwargs["padx"][0], 0)
            lbl_kwargs["padx"] = (0, 0)

        self._btn_up.grid(row=self._index, column=0, **self._grid_kwargs)
        self._btn_down.grid(row=self._index, column=1, sticky="nsew", **self._grid_kwargs)
        self._om_commands.grid(row=self._index, column=2, sticky="nsew", **self._grid_kwargs)
        self._e_input.grid(row=self._index, column=3, sticky="nsew", **pre_lbl_kwargs)
        self._lbl_input.grid(row=self._index, column=4, sticky="nsew", **lbl_kwargs)
        self._e_output.grid(row=self._index, column=5, sticky="nsew", **pre_lbl_kwargs)
        self._lbl_output.grid(row=self._index, column=6, sticky="nsew", **lbl_kwargs)
        self._chk_special.grid(row=self._index, column=7, sticky="nsew", **self._grid_kwargs)
        self._sb_special.grid(row=self._index, column=8, sticky="nsew", **self._grid_kwargs)
        self._btn_params.grid(row=self._index, column=9, sticky="nsew", **pre_lbl_kwargs)
        self._lbl_params.grid(row=self._index, column=10, sticky="nsew", **lbl_kwargs)
        self._btn_info.grid(row=self._index, column=11, sticky="nsew", **self._grid_kwargs)
        self._btn_remove.grid(row=self._index, column=12, **self._grid_kwargs)

    def destroy(self) -> None:
        self._btn_up.destroy()
        self._btn_down.destroy()
        self._om_commands.destroy()
        self._e_input.destroy()
        self._lbl_input.destroy()
        self._e_output.destroy()
        self._lbl_output.destroy()
        self._chk_special.destroy()
        self._sb_special.destroy()
        self._btn_params.destroy()
        self._lbl_params.destroy()
        self._btn_info.destroy()
        self._btn_remove.destroy()

        self._command_config.remove_callback(self._on_command_config_change)
        self._pipeline_configuration.pipeline.remove_callback(self._on_pipeline_change)

    def _get_special_value(self) -> Optional[int]:
        try:
            return int(self._sb_special.get())
        except ValueError:
            return None

    def _on_command_config_change(self, _: CommandConfiguration, event: CommandConfigurationEvent) -> None:
        if event.attribute == CommandConfiguration.command.fget.__name__:  # type: ignore
            self._update_command()
        elif event.attribute == CommandConfiguration.input_dir.fget.__name__:  # type: ignore
            self._update_input_dir()
        elif event.attribute == CommandConfiguration.output_dir.fget.__name__:  # type: ignore
            self._update_output_dir()
        elif event.attribute == CommandConfiguration.special.fget.__name__:  # type: ignore
            self._update_special()
        elif event.attribute.startswith("param_values"):
            self._update_params()

    def _on_pipeline_change(self, _: Pipeline, event: PipelineChangeEvent) -> None:
        if event.action == PipelineChangeType.ADD or event.action == PipelineChangeType.INSERT:
            if self._index >= event.index:
                self._index += 1
                self._update_position()
            else:
                self._update_arrows()
        elif event.action == PipelineChangeType.REMOVE:
            if self._index == event.index:
                self.destroy()
            elif self._index > event.index:
                self._index -= 1
                self._update_position()
        elif event.action == PipelineChangeType.SWAP:
            if self._index == event.index_a:
                self._index = event.index_b  # type: ignore
                self._update_position()
            elif self._index == event.index_b:
                self._index = event.index_a
                self._update_position()

    def _on_command_change(self, variable: str, _, action: str):
        if self._command_config.command.name != self._sv_om_commands.get():
            new_command = self._commands.find_by_name(self._sv_om_commands.get())
            new_configuration = CommandConfiguration(new_command)

            self._command_config.copy_to(new_configuration)

            self._pipeline_configuration.replace_command_configuration(self._index, new_configuration)

    def _on_input_change(self, event: Event) -> None:
        new_dir = event.widget.get().strip()
        self._command_config.input_dir = new_dir

        if len(new_dir) == 0:
            self._sv_lbl_input.set("!")
        else:
            self._sv_lbl_input.set("")

    def _on_output_change(self, event: Event) -> None:
        new_dir = event.widget.get().strip()
        self._command_config.output_dir = new_dir

        if len(new_dir) == 0:
            self._sv_lbl_output.set("!")
        else:
            self._sv_lbl_output.set("")

    def _on_special_activation_change(self) -> None:
        if self._bv_chk_special.get():
            self._sb_special.configure(state=NORMAL)
            self._command_config.special = self._get_special_value()
        else:
            self._command_config.special = None
            self._sb_special.configure(state=DISABLED)

    def _on_special_change(self, _: Optional[Event] = None) -> None:
        self._command_config.special = self._get_special_value()

    def _on_down_command(self) -> None:
        self._pipeline_configuration.pipeline.swap_command_position(self._index, self._index + 1)

    def _on_up_command(self) -> None:
        self._pipeline_configuration.pipeline.swap_command_position(self._index, self._index - 1)

    def _on_remove_command(self) -> None:
        self._pipeline_configuration.pipeline.remove_command(self._index)

    def _on_params_command(self) -> None:
        dialog = ParamConfigurationDialog(self._command_config, self._master)
        dialog.wait_visibility()
        dialog.grab_set()

    def _on_info_command(self) -> None:
        if "DOCKER_BROWSER_FIFO" in os.environ:
            fifo = os.environ["DOCKER_BROWSER_FIFO"]
            with open(fifo, "a") as fifo_file:
                fifo_file.write(self._command_config.command.url + "\n")
                fifo_file.flush()
        else:
            webbrowser.open(self._command_config.command.url)

    def _update_position(self):
        self._update_arrows()

        self._locate_components()

    def _update_arrows(self):
        self._btn_up.config(state=DISABLED if self._index == 0 else NORMAL)
        self._btn_down.config(
            state=DISABLED if self._index == len(self._pipeline_configuration.pipeline) - 1 else NORMAL)

    def _update_command(self) -> None:
        self._sv_om_commands.set(self._command_config.command.name)

        if self._command_config.command.supports_special:
            if self._command_config.has_special():
                self._bv_chk_special.set(True)
                self._sb_special.set(self._command_config.special)
            else:
                self._bv_chk_special.set(False)
                self._sb_special.set("")

            self._sb_special.configure(state=NORMAL)
            self._chk_special.configure(state=NORMAL)
        else:
            self._sb_special.set("")
            self._bv_chk_special.set(False)
            self._sb_special.configure(state=DISABLED)
            self._chk_special.configure(state=DISABLED)

        if self._command_config.command.has_params():
            self._btn_params.configure(state=NORMAL)
        else:
            self._btn_params.configure(state=DISABLED)

    def _update_input_dir(self) -> None:
        self._e_input.delete(0, len(self._e_input.get()))
        if self._command_config.has_input_dir():
            self._e_input.insert(0, self._command_config.input_dir)  # type: ignore
            self._sv_lbl_input.set(" ")
        else:
            self._sv_lbl_input.set("!")

    def _update_output_dir(self) -> None:
        self._e_output.delete(0, len(self._e_output.get()))
        if self._command_config.has_output_dir():
            self._e_output.insert(0, self._command_config.output_dir)  # type: ignore
            self._sv_lbl_output.set(" ")
        else:
            self._sv_lbl_output.set("!")

    def _update_special(self) -> None:
        if not self._command_config.is_special_supported():
            self._chk_special.config(state=DISABLED)
            self._sb_special.config(state=DISABLED)  # type: ignore
        else:
            if self._command_config.has_special():
                self._bv_chk_special.set(True)
                self._sb_special.config(state=NORMAL)  # type: ignore
                self._sb_special.set(self._command_config.special)
            else:
                self._bv_chk_special.set(False)
                self._sb_special.config(state=DISABLED)  # type: ignore

    def _update_params(self) -> None:
        if self._command_config.is_valid_config():
            self._sv_lbl_params.set(" ")
        else:
            self._sv_lbl_params.set("!")
