from auto_phylo.pipeliner.io.ParseError import ParseError as ParseError
from tkinter import Misc, Toplevel
from typing import Optional

class ParseErrorViewerDialog(Toplevel):
    def __init__(self, title: str, parsed_text: str, parse_error: ParseError, master: Optional[Misc] = ...) -> None: ...
