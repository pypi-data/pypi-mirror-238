import stat
from pathlib import Path
from tkinter import Tk, filedialog, StringVar, Misc, Entry, Text, Event
from tkinter.constants import BOTH, X, TOP, FLAT, LEFT, RIGHT, Y, DISABLED, NORMAL, INSERT, END
from tkinter.messagebox import askyesno, askyesnocancel, showerror, WARNING
from tkinter.ttk import Notebook, Frame, Label, Button, Style
from typing import Optional, Tuple, Final

import sv_ttk

from auto_phylo.pipeliner import load_commands
from auto_phylo.pipeliner.component.ParseErrorViewerDialog import ParseErrorViewerDialog
from auto_phylo.pipeliner.component.PipelineDesigner import PipelineDesigner
from auto_phylo.pipeliner.io.ConfigurationGenerator import ConfigurationGenerator
from auto_phylo.pipeliner.io.ConfigurationParser import ConfigurationParser
from auto_phylo.pipeliner.io.ParseError import ParseError
from auto_phylo.pipeliner.io.PipelineGenerator import PipelineGenerator
from auto_phylo.pipeliner.io.PipelineParser import PipelineParser
from auto_phylo.pipeliner.io.RunFileGenerator import RunFileGenerator
from auto_phylo.pipeliner.io.RunFileParser import RunFileParser
from auto_phylo.pipeliner.model.Commands import Commands
from auto_phylo.pipeliner.model.Pipeline import Pipeline
from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration
from auto_phylo.pipeliner.model.PipelineConfigurationChangeEvent import PipelineConfigurationChangeEvent
from auto_phylo.pipeliner.util.EventListeners import EventListeners, EventQueue


def _directory_has_pipeline_files(directory: str) -> bool:
    path = Path(directory)

    sub_paths = [
        path / "config",
        path / "pipeline",
        path / "run.sh"
    ]

    return any(sub_path.is_file() for sub_path in sub_paths)


class AutoPhyloPipeliner(Tk):
    _COLOR_ERROR: Final[str] = "#ffcccc"

    def __init__(self,
                 pipeline_configuration: Optional[PipelineConfiguration] = None,
                 commands: Commands = load_commands(),
                 auto_phylo_version: str = "2.0.0",
                 *args, **kwargs):
        super().__init__(*args, *kwargs)

        self._commands: Commands = commands
        self._pipeline_configuration: Optional[PipelineConfiguration] = pipeline_configuration
        self._auto_phylo_version: str = auto_phylo_version

        self._pipeline_generator: PipelineGenerator = PipelineGenerator()
        self._configuration_generator: ConfigurationGenerator = ConfigurationGenerator()
        self._run_file_generator: RunFileGenerator = RunFileGenerator()

        self._pipeline_parser: PipelineParser = PipelineParser(self._commands)
        self._configuration_parser: ConfigurationParser = ConfigurationParser()
        self._run_file_parser: RunFileParser = RunFileParser()

        self.title("auto-phylo-pipeliner")
        sv_ttk.use_light_theme()

        self._toolbar: _Toolbar = _Toolbar(auto_phylo_version, self)
        self._tab_control: Notebook = Notebook(self)
        self._status_bar: _StatusBar = _StatusBar("Welcome to auto-phylo-pipeliner")

        self._frm_designer: Frame = Frame(self._tab_control)
        self._frm_pipeline: Frame = Frame(self._tab_control)
        self._frm_config: Frame = Frame(self._tab_control)

        self._panel_designer: Optional[_DesignerFrame] = None
        self._text_pipeline: Optional[Text] = None
        self._text_config: Optional[Text] = None

        self._frm_designer.pack(expand=True, fill=BOTH)
        self._frm_pipeline.pack(expand=True, fill=BOTH)
        self._frm_config.pack(expand=True, fill=BOTH)

        self._tab_control.add(self._frm_designer, text="Designer")
        self._tab_control.add(self._frm_pipeline, text="Pipeline")
        self._tab_control.add(self._frm_config, text="Configuration")

        self._toolbar.pack(expand=False, fill=X, padx=2, pady=4)
        self._tab_control.pack(expand=True, fill=BOTH)
        self._status_bar.pack(expand=False, fill=X)

        self._update_components()
        self._update_texts()

        self._toolbar.event_new_pipeline.add_callback(self._on_new_pipeline)
        self._toolbar.event_auto_phylo_version_change.add_callback(self._on_auto_phylo_version_change)
        if self._pipeline_configuration is not None:
            self._pipeline_configuration.add_callback(self._on_pipeline_config_change)

    def _on_pipeline_config_change(self, _: PipelineConfiguration, __: PipelineConfigurationChangeEvent) -> None:
        if self._pipeline_configuration is None:
            raise RuntimeError("pipeline_config should now be None")

        self._update_texts()
        self._update_files()
        self._update_pipeline_status()

    def _on_auto_phylo_version_change(self, auto_phylo_version: str) -> None:
        if self._auto_phylo_version != auto_phylo_version:
            self._auto_phylo_version = auto_phylo_version
            self._update_run_file()
            self._status_bar.message = "Run file updated"

    def _on_new_pipeline(self, directory: Tuple[str, bool]) -> None:
        pipeline_dir, load = directory

        if self._pipeline_configuration is not None:
            self._pipeline_configuration.remove_callback(self._on_pipeline_config_change)

            for main_frm in [self._frm_designer, self._frm_pipeline, self._frm_config]:
                for child in main_frm.winfo_children():
                    child.destroy()

        if load:
            directory_path = Path(pipeline_dir)
            pipeline_path = directory_path / "pipeline"
            config_path = directory_path / "config"
            run_file_path = directory_path / "run.sh"

            if not pipeline_path.is_file():
                showerror("Missing pipeline file", "Pipeline could not be loaded because the pipeline file is missing.")
                return

            if not config_path.is_file():
                showerror("Missing config file", "Pipeline could not be loaded because the config file is missing.")
                return

            if not run_file_path.is_file():
                if not askyesno("Missing run file",
                                "The run file is missing. Do you want to create a new one?\n\n"
                                "(If 'No' is selected pipeline loading will be cancelled)",
                                icon=WARNING):
                    return

            try:
                with pipeline_path.open("r") as pipeline_file:
                    pipeline_configuration = self._pipeline_parser.parse(pipeline_file)
            except ParseError as pe:
                with pipeline_path.open("r") as pipeline_file:
                    viewer = ParseErrorViewerDialog("Pipeline error", pipeline_file.read(), pe, self)
                    viewer.grab_set()
                    viewer.wait_window()
                    return

            try:
                with config_path.open("r") as config_file:
                    pipeline_configuration = self._configuration_parser.parse(config_file, pipeline_configuration)
            except ParseError as pe:
                with config_path.open("r") as config_file:
                    viewer = ParseErrorViewerDialog("Configuration error", config_file.read(), pe, self)
                    viewer.grab_set()
                    viewer.wait_window()
                    return

            create_run_file = False
            if run_file_path.is_file():
                try:
                    with run_file_path.open("r") as run_file_file:
                        self._toolbar.auto_phylo_version = self._run_file_parser.parse(run_file_file)
                except ParseError:
                    if askyesno("Error loading run file",
                                "The run file is not valid. Do you want to generate a new one?\n\n"
                                "(If 'No' is selected pipeline loading will be cancelled)",
                                icon=WARNING):
                        create_run_file = True
                    else:
                        return

            if pipeline_configuration.output_dir is None:
                raise RuntimeError("pipeline_configuration.output_dir should not be None")

            if Path(pipeline_configuration.output_dir).absolute() != Path(pipeline_dir).absolute():
                if askyesno("Directory mismatch",
                            "The config file 'dir' does not match the pipeline directory. "
                            "To solve this, 'dir' will be changed to match the pipeline directory. "
                            "Do you want to continue?\n\n"
                            "(If 'No' is selected pipeline loading will be cancelled)",
                            icon=WARNING):
                    pipeline_configuration.output_dir = pipeline_dir

            self._pipeline_configuration = pipeline_configuration

            if create_run_file:
                self._update_run_file()
        else:
            self._pipeline_configuration = PipelineConfiguration(Pipeline(), output_dir=directory[0],
                                                                 seda_version="\"seda:1.6.0-SNAPSHOT-20230920.1\"")

        self._update_components()
        self._update_texts()
        self._update_files()
        self._update_pipeline_status()

        self._pipeline_configuration.add_callback(self._on_pipeline_config_change)

    def _update_components(self) -> None:
        if self._pipeline_configuration is None:
            self._tab_control.select(0)

            for main_frm in [self._frm_designer, self._frm_pipeline, self._frm_config]:
                for child in main_frm.winfo_children():
                    child.destroy()

            for index in range(0, len(self._tab_control.tabs())):
                self._tab_control.tab(index, state=DISABLED)
        else:
            for index in range(0, len(self._tab_control.tabs())):
                self._tab_control.tab(index, state=NORMAL)

            self._panel_designer = _DesignerFrame(self._pipeline_configuration, self._commands, self._frm_designer)
            self._text_pipeline = Text(self._frm_pipeline, state=DISABLED, spacing3=4)
            self._text_config = Text(self._frm_config, state=DISABLED, spacing3=4)

            self._panel_designer.pack(expand=True, fill=BOTH)
            self._text_pipeline.pack(expand=True, fill=BOTH)
            self._text_config.pack(expand=True, fill=BOTH)

            self._tab_control.select(0)

    def _update_texts(self) -> None:
        if self._pipeline_configuration is None:
            return

        if self._text_pipeline is None or self._text_config is None:
            raise RuntimeError("text_pipeline and text_config should not be None")

        self._text_pipeline.configure(state=NORMAL)
        self._text_config.configure(state=NORMAL)

        self._text_pipeline.delete("1.0", END)
        self._text_config.delete("1.0", END)

        if self._pipeline_configuration.is_valid_pipeline():
            self._text_pipeline["bg"] = "#ffffff"

            pipeline_text = self._pipeline_generator.generate(self._pipeline_configuration)
            self._text_pipeline.insert(INSERT, pipeline_text)
        else:
            self._text_pipeline["bg"] = AutoPhyloPipeliner._COLOR_ERROR
            self._text_pipeline.insert(INSERT, "Pipeline is not valid")

        if self._pipeline_configuration.is_valid_config():
            self._text_config["bg"] = "#ffffff"
        else:
            self._text_config["bg"] = AutoPhyloPipeliner._COLOR_ERROR

        config_text = self._configuration_generator.generate(self._pipeline_configuration)
        self._text_config.insert(INSERT, config_text)

        self._text_pipeline.configure(state=DISABLED)
        self._text_config.configure(state=DISABLED)

    def _update_files(self) -> None:
        if self._pipeline_configuration is None:
            return

        if self._pipeline_configuration.is_valid_pipeline():
            if self._pipeline_configuration.output_dir is None:
                raise ValueError("pipeline_configuration.output_dir should not be None")

            working_path = Path(self._pipeline_configuration.output_dir)
            pipeline_path = working_path / "pipeline"
            config_path = working_path / "config"

            with pipeline_path.open("w") as pipeline_file:
                pipeline_file.write(self._pipeline_generator.generate(self._pipeline_configuration))

            with config_path.open("w") as config_file:
                config_file.write(self._configuration_generator.generate(self._pipeline_configuration))

        self._update_run_file()

    def _update_run_file(self) -> None:
        if self._pipeline_configuration is None:
            return

        if self._pipeline_configuration.output_dir is None:
            raise ValueError("pipeline_configuration.output_dir should not be None")

        working_path = Path(self._pipeline_configuration.output_dir)
        run_file_path = working_path / "run.sh"

        with run_file_path.open("w") as run_file_file:
            run_file_file.write(
                self._run_file_generator.generate(self._pipeline_configuration, self._auto_phylo_version))

        # Gives execution permissions for the file owner
        current_permissions = run_file_path.stat().st_mode
        new_permissions = current_permissions | stat.S_IXUSR
        run_file_path.chmod(new_permissions)

    def _update_pipeline_status(self):
        if self._pipeline_configuration is not None:
            valid_pipeline = self._pipeline_configuration.is_valid_pipeline()
            valid_config = self._pipeline_configuration.is_valid_config()

            if valid_pipeline and valid_config:
                self._status_bar.set_ok("Pipeline and configuration are valid")
            elif not valid_pipeline and not valid_config:
                self._status_bar.set_error("Pipeline and configuration are incomplete")
            elif not valid_pipeline:
                self._status_bar.set_warning("Pipeline is incomplete")
            elif not valid_config:  # Yes, you don't really have to check this
                self._status_bar.set_warning("Configuration is incomplete")


class _Toolbar(Frame):
    def __init__(self, auto_phylo_version: str, master: Optional[Misc] = None, relief=FLAT, *args, **kwargs):
        super().__init__(master, relief=relief, *args, **kwargs)

        self._queue_new_pipeline: EventQueue[Tuple[str, bool]] = EventQueue[Tuple[str, bool]]()
        self._event_new_pipeline: EventListeners[Tuple[str, bool]] = \
            EventListeners[Tuple[str, bool]](self._queue_new_pipeline)

        self._queue_auto_phylo_version_change: EventQueue[str] = EventQueue[str]()
        self._event_auto_phylo_version_change: EventListeners[str] = \
            EventListeners[str](self._queue_auto_phylo_version_change)

        self._build_components(auto_phylo_version)

    def _build_components(self, auto_phylo_version: str):
        btn_new_pipeline = Button(self, text="Load / Create pipeline", command=self._on_new_pipeline)
        btn_change_theme = Button(self, text="Change theme", command=sv_ttk.toggle_theme)

        lbl_auto_phylo_version = Label(self, text="Auto-phylo version")
        self._sv_e_auto_phylo_version: StringVar = StringVar(self, value=auto_phylo_version)
        e_auto_phylo_version = Entry(self, textvariable=self._sv_e_auto_phylo_version)

        e_auto_phylo_version.bind("<FocusOut>", self._on_auto_phylo_version_change)

        btn_new_pipeline.pack(side=LEFT, padx=2, pady=2)
        btn_change_theme.pack(side=LEFT, padx=2, pady=2)
        e_auto_phylo_version.pack(side=RIGHT, padx=2, pady=2, fill=Y)
        lbl_auto_phylo_version.pack(side=RIGHT, padx=2, pady=2)

    @property
    def auto_phylo_version(self) -> str:
        return self._sv_e_auto_phylo_version.get()

    @auto_phylo_version.setter
    def auto_phylo_version(self, auto_phylo_version: str) -> None:
        if self.auto_phylo_version != auto_phylo_version:
            self._sv_e_auto_phylo_version.set(auto_phylo_version)

    @property
    def event_new_pipeline(self) -> EventListeners[Tuple[str, bool]]:
        return self._event_new_pipeline

    @property
    def event_auto_phylo_version_change(self) -> EventListeners[str]:
        return self._event_auto_phylo_version_change

    def _on_new_pipeline(self) -> None:
        selected_directory = filedialog.askdirectory(parent=self)

        if not selected_directory:
            return

        if _directory_has_pipeline_files(selected_directory):
            load = askyesnocancel("Directory conflict",
                                  "The directory already contains a pipeline configuration. Do you want to load it?\n\n"
                                  "(If 'No' is selected files will be overwritten)")
            if load is None:
                return
        else:
            load = False

        self._queue_new_pipeline.notify((selected_directory, load))

    def _on_auto_phylo_version_change(self, event: Event) -> None:
        self._queue_auto_phylo_version_change.notify(event.widget.get())


class _DesignerFrame(Frame):
    def __init__(self, pipeline_configuration: PipelineConfiguration, commands: Commands = load_commands(),
                 master: Optional[Misc] = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._pipeline_configuration: PipelineConfiguration = pipeline_configuration

        self._top_frame: Frame = Frame(self)
        self._center_frame: PipelineDesigner = PipelineDesigner(self._pipeline_configuration, commands, self)

        self._sv_btn_working_dir: StringVar = StringVar()
        self._btn_working_dir: Button = Button(self._top_frame, textvariable=self._sv_btn_working_dir,
                                               command=self._on_change_working_dir)
        self._sv_lbl_working_dir: StringVar = StringVar()
        self._lbl_working_dir: Label = Label(self._top_frame, textvariable=self._sv_lbl_working_dir)

        self._lbl_seda_version: Label = Label(self._top_frame, text="SEDA version")
        self._sv_e_seda_version: StringVar = StringVar(self._top_frame, value=pipeline_configuration.seda_version)
        self._e_seda_version: Entry = Entry(self._top_frame, textvariable=self._sv_e_seda_version)
        self._e_seda_version.bind("<FocusOut>", self._on_seda_version_change)

        self._lbl_working_dir.pack(side=LEFT, padx=4)
        self._btn_working_dir.pack(side=LEFT, padx=4)

        self._e_seda_version.pack(side=RIGHT, fill=Y, padx=4)
        self._lbl_seda_version.pack(side=RIGHT, padx=4)

        self._top_frame.pack(side=TOP, pady=(8, 12), fill=X)
        self._center_frame.pack(side=TOP, pady=4, padx=4, fill=BOTH, expand=True)

        self._update_pipeline_config()

        self._pipeline_configuration.add_callback(self._on_pipeline_configuration_change)

    @property
    def pipeline_configuration(self) -> PipelineConfiguration:
        return self._pipeline_configuration

    @pipeline_configuration.setter
    def pipeline_configuration(self, pipeline_config: PipelineConfiguration) -> None:
        if self._pipeline_configuration != pipeline_config:
            self._update_pipeline_config()

    def _update_pipeline_config(self) -> None:
        self._update_working_dir_components()

        self._center_frame.pipeline_configuration = self._pipeline_configuration

    def _update_working_dir_components(self):
        if self._pipeline_configuration.output_dir is None:
            self._sv_btn_working_dir.set("Select")
            self._sv_lbl_working_dir.set("<No working directory selected>")
        else:
            self._sv_btn_working_dir.set("Change")
            self._sv_lbl_working_dir.set(f"Working directory: {self._pipeline_configuration.output_dir}")

    def _update_seda_version_components(self):
        if self._pipeline_configuration.seda_version is None:
            self._sv_e_seda_version.set("")
        else:
            self._sv_e_seda_version.set(self._pipeline_configuration.seda_version)

    def _on_change_working_dir(self) -> None:
        selected_directory = filedialog.askdirectory(initialdir=self._pipeline_configuration.output_dir)

        if _directory_has_pipeline_files(selected_directory):
            if not askyesno("Directory conflict",
                            "The directory already contains a pipeline configuration. Do you want to overwrite it?"):
                return

        self._pipeline_configuration.output_dir = selected_directory

    def _on_seda_version_change(self, _: Event) -> None:
        self._pipeline_configuration.seda_version = self._sv_e_seda_version.get()

    def _on_pipeline_configuration_change(self, _: PipelineConfiguration,
                                          event: PipelineConfigurationChangeEvent) -> None:
        if event.attribute == PipelineConfiguration.output_dir.fget.__name__:  # type: ignore
            self._update_working_dir_components()
        elif event.attribute == PipelineConfiguration.seda_version.fget.__name__:  # type: ignore
            self._update_seda_version_components()


class _StatusBar(Frame):
    _COLOR_OK: Final[str] = "#aaffaa"
    _STYLE_OK_FRAME: Final[str] = "AutoPhyloPipeliner_StatusBar_Ok.TFrame"
    _STYLE_OK_LABEL: Final[str] = "AutoPhyloPipeliner_StatusBar_Ok.TLabel"

    _COLOR_WARNING: Final[str] = "#ffccaa"
    _STYLE_WARNING_FRAME: Final[str] = "AutoPhyloPipeliner_StatusBar_Warning.TFrame"
    _STYLE_WARNING_LABEL: Final[str] = "AutoPhyloPipeliner_StatusBar_Warning.TLabel"

    _COLOR_ERROR: Final[str] = "#ffaaaa"
    _STYLE_ERROR_FRAME: Final[str] = "AutoPhyloPipeliner_StatusBar_Error.TFrame"
    _STYLE_ERROR_LABEL: Final[str] = "AutoPhyloPipeliner_StatusBar_Error.TLabel"

    def __init__(self, initial_message: str = "", master: Optional[Misc] = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._style: Style = Style()
        self._style.configure(_StatusBar._STYLE_OK_FRAME, background=_StatusBar._COLOR_OK)
        self._style.configure(_StatusBar._STYLE_OK_LABEL, background=_StatusBar._COLOR_OK)
        self._style.configure(_StatusBar._STYLE_WARNING_FRAME, background=_StatusBar._COLOR_WARNING)
        self._style.configure(_StatusBar._STYLE_WARNING_LABEL, background=_StatusBar._COLOR_WARNING)
        self._style.configure(_StatusBar._STYLE_ERROR_FRAME, background=_StatusBar._COLOR_ERROR)
        self._style.configure(_StatusBar._STYLE_ERROR_LABEL, background=_StatusBar._COLOR_ERROR)

        self._sb_lbl_status: StringVar = StringVar()
        self._sb_lbl_status.set(initial_message)
        self._lbl_status = Label(self, textvariable=self._sb_lbl_status)

        self._lbl_status.pack(expand=True, fill=BOTH, pady=4, padx=4)

    @property
    def message(self) -> str:
        return self._sb_lbl_status.get()

    @message.setter
    def message(self, message: str) -> None:
        self._sb_lbl_status.set(message)
        self.configure(style="TFrame")
        self._lbl_status.configure(style="TLabel")

    def set_warning(self, message: str) -> None:
        self._sb_lbl_status.set(message)
        self.configure(style=_StatusBar._STYLE_WARNING_FRAME)
        self._lbl_status.configure(style=_StatusBar._STYLE_WARNING_LABEL)

    def set_error(self, message: str) -> None:
        self._sb_lbl_status.set(message)
        self.configure(style=_StatusBar._STYLE_ERROR_FRAME)
        self._lbl_status.configure(style=_StatusBar._STYLE_ERROR_LABEL)

    def set_ok(self, message: str) -> None:
        self._sb_lbl_status.set(message)
        self.configure(style=_StatusBar._STYLE_OK_FRAME)
        self._lbl_status.configure(style=_StatusBar._STYLE_OK_LABEL)
