from pathlib import Path

from auto_phylo.pipeliner.io import strip_lines
from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration


class RunFileGenerator:
    def generate(self, pipeline: PipelineConfiguration, auto_phylo_version: str) -> str:
        if pipeline.output_dir is None:
            raise ValueError("pipeline.output_dir can't be None")

        path = Path(pipeline.output_dir).absolute()

        output = f"""
#!/bin/bash

docker run --rm -v "{path}":/data -v /var/run/docker.sock:/var/run/docker.sock pegi3s/auto-phylo:{auto_phylo_version}
"""

        return strip_lines(output)
