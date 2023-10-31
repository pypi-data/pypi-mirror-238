import re
from typing import TextIO, Dict, List

from auto_phylo.pipeliner import load_commands
from auto_phylo.pipeliner.io.ParseError import ParseError
from auto_phylo.pipeliner.model.CommandConfiguration import CommandConfiguration
from auto_phylo.pipeliner.model.Commands import Commands
from auto_phylo.pipeliner.model.Pipeline import Pipeline
from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration


class PipelineParser:
    def __init__(self, commands: Commands = load_commands()):
        self._commands: Commands = commands

    def parse(self, text: TextIO) -> PipelineConfiguration:
        pipeline: Pipeline = Pipeline()
        command_configurations: List[CommandConfiguration] = []

        errors: Dict[int, str] = {}
        line_regex = r"(\S+) (\S+) (\S+)(?: Special ([0-9]+))?"

        for line_number, line in enumerate(text):
            line = line.strip()

            if len(line) == 0 or line.startswith("#"):
                continue

            match = re.fullmatch(line_regex, line)

            if match is None:
                errors[line_number] = ("Invalid property. Config must be specified using a "
                                       "'<tool> <in dir> <out dir> [Special <val>]' format")
            else:
                tool_name, input_dir, output_dir, special_value = match.groups()

                try:
                    tool = self._commands.find_by_tool(tool_name)
                except LookupError:
                    errors[line_number] = f"Unknown tool: {tool_name}"
                    continue

                if special_value is not None:
                    if not tool.supports_special:
                        errors[line_number] = f"Tool {tool_name} does not support special."
                        continue

                    if not special_value.isdigit():
                        errors[line_number] = "Invalid special value. Only positive integers are allowed."
                        continue

                pipeline.add_command(tool)
                command_configurations.append(
                    CommandConfiguration(
                        tool, input_dir, output_dir,
                        int(special_value) if special_value is not None else None
                    )
                )

        if len(errors) > 0:
            raise ParseError(errors)

        return PipelineConfiguration(pipeline, command_configs=command_configurations)
