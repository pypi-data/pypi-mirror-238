import re
from typing import TextIO

from auto_phylo.pipeliner.io.ParseError import ParseError


class RunFileParser:
    def parse(self, text: TextIO) -> str:
        line_regex = r"docker run .* pegi3s/auto-phylo:(.*)"

        for line_number, line in enumerate(text):
            line = line.strip()

            match = re.fullmatch(line_regex, line)

            if match is not None:
                return match.groups()[0]

        raise ParseError(general_errors=["Missing Auto-phylo version"])
