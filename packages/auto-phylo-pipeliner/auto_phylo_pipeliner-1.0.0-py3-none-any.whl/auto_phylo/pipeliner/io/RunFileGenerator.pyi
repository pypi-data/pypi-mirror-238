from auto_phylo.pipeliner.model.PipelineConfiguration import PipelineConfiguration as PipelineConfiguration

class RunFileGenerator:
    def generate(self, pipeline: PipelineConfiguration, auto_phylo_version: str) -> str: ...
