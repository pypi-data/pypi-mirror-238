import re
from typing import TextIO, Dict

from auto_phylo.pipeliner.io.ParseError import ParseError
from auto_phylo.pipeliner.model.CommandConfiguration import CommandConfiguration
from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration


class ConfigurationParser:
    def parse(self, text: TextIO, pipeline_configuration: PipelineConfiguration) -> PipelineConfiguration:
        errors: Dict[int, str] = {}
        line_regex = r"([^=]+)=([^=]*)"
        general_errors = []

        for line_number, line in enumerate(text):
            line = line.strip()

            if len(line) == 0 or line.startswith("#"):
                continue

            match = re.fullmatch(line_regex, line)

            if match is None:
                errors[line_number] = "Invalid property. Properties must be specified using a <key>=<value> format"
            else:
                if len(match.groups()) == 2:
                    param = match.groups()[0].strip()
                    value = match.groups()[1].strip()
                else:
                    param = match.groups()[0].strip()
                    value = ""

                if param == "SEDA":
                    if len(value) == 0:
                        errors[line_number] = "SEDA must have a value"
                    else:
                        pipeline_configuration.seda_version = value
                elif param == "dir":
                    if len(value) == 0:
                        errors[line_number] = "dir must have a value"
                    else:
                        pipeline_configuration.output_dir = value
                else:
                    try:
                        command = pipeline_configuration.pipeline.find_command_with_param(param)
                        pipeline_configuration.set_command_param_value(command, param, value)
                    except ValueError:
                        errors[line_number] = f"Pipeline configuration has no command for param {param}"

        if pipeline_configuration.seda_version is None:
            general_errors.append("Missing SEDA version")

        if pipeline_configuration.output_dir is None:
            general_errors.append("Missing working directory (dir)")

        if len(errors) > 0 or len(general_errors) > 0:
            raise ParseError(
                errors if len(errors) > 0 else None,
                general_errors if len(general_errors) > 0 else None
            )

        return pipeline_configuration
