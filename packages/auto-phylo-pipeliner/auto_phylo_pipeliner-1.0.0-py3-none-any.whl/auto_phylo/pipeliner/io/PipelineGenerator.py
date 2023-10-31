from auto_phylo.pipeliner.io import strip_lines
from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration


class PipelineGenerator:
    def generate(self, pipeline: PipelineConfiguration) -> str:
        output = ""

        for index, command in enumerate(pipeline.pipeline):
            config = pipeline.get_command_configuration(index)

            output += f"{command.tool} {config.input_dir} {config.output_dir}"

            if command.supports_special and config.has_special():
                output += f" Special {config.special}"

            output += "\n"

        return strip_lines(output)
