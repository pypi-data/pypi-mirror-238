from typing import Dict

from auto_phylo.pipeliner.io import strip_lines
from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration


class ConfigurationGenerator:
    def generate(self, pipeline: PipelineConfiguration) -> str:
        output = f"""
# General parameters
SEDA={pipeline.seda_version}
dir={pipeline.output_dir}

# Other parameters
"""

        for command in pipeline.pipeline:
            param_values: Dict[str, str] = pipeline.get_command_param_values(command)

            if len(param_values) > 0:
                output += f"# {command.tool}\n"

                for param in pipeline.list_command_param_names(command):
                    output += f"{param}={param_values[param]}\n"

                output += "\n"

        return strip_lines(output)
