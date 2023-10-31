from tkinter import Toplevel, Misc, Text, INSERT, BOTH, DISABLED, Event, StringVar
from tkinter.constants import X, CURRENT
from tkinter.font import NORMAL
from tkinter.ttk import Label, Button
from typing import Optional, List

from auto_phylo.pipeliner.io.ParseError import ParseError


class ParseErrorViewerDialog(Toplevel):
    def __init__(self, title: str, parsed_text: str, parse_error: ParseError, master: Optional[Misc] = None):
        super().__init__(master)

        self.title(title)

        self._parsed_text: str = parsed_text
        self._parse_error: ParseError = parse_error

        self._numbered_lines: List[str] = self._numerate_lines(parsed_text.splitlines())
        self._numbered_text: str = "\n".join(self._numbered_lines)

        self._sv_lbl_general_errors: StringVar = StringVar()
        self._lbl_general_errors: Label = Label(self, textvariable=self._sv_lbl_general_errors, padding=(4, 4))

        self._txt_parsed_text: Text = Text(self, font=("Monospaced", 10, NORMAL))
        self._default_cursor: str = self._txt_parsed_text["cursor"]
        self._txt_parsed_text.insert(INSERT, self._numbered_text)

        self._sv_lbl_line_error: StringVar = StringVar()
        self._lbl_line_error: Label = Label(self, textvariable=self._sv_lbl_line_error, padding=(4, 4))

        self._btn_close: Button = Button(self, text="Close", command=self.destroy)

        if self._parse_error.general_errors is None:
            self._sv_lbl_general_errors.set("The file could not be loaded because it contains some errors.")
        else:
            message = ("The file could not be loaded because it contains some errors.\n\n"
                       "The following general errors have been found:\n  - ")
            message += "\n  - ".join(self._parse_error.general_errors)
            self._sv_lbl_general_errors.set(message)

        if parse_error.line_errors is not None:
            max_error_length = 0
            for index, line in parse_error.line_errors.items():
                max_error_length = max(max_error_length, len(line))
                tag_id = str(index)
                index += 1

                self._txt_parsed_text.tag_add(tag_id, f"{index}.0", f"{index}.end")
                self._txt_parsed_text.tag_config(tag_id, background="#ffaaaa")

                self._txt_parsed_text.tag_bind(tag_id, "<Enter>", self._on_tag_enter)
                self._txt_parsed_text.tag_bind(tag_id, "<Leave>", self._on_tag_leave)

            self._lbl_line_error.configure(width=max_error_length)

        self._txt_parsed_text.configure(state=DISABLED)

        self._lbl_general_errors.pack(fill=X, pady=2)
        self._txt_parsed_text.pack(expand=True, fill=BOTH, pady=2)
        self._lbl_line_error.pack(fill=X, pady=2)
        self._btn_close.pack(pady=4)

    def _on_tag_enter(self, _: Event) -> None:
        cursor_index = self._txt_parsed_text.index(CURRENT)
        tag = self._txt_parsed_text.tag_names(cursor_index)[0]
        index = int(tag)

        if self._parse_error.line_errors is None:
            raise RuntimeError("parse_error should have line_errors")

        self._sv_lbl_line_error.set(self._parse_error.line_errors[index])

        self._txt_parsed_text.config(cursor="arrow")

    def _on_tag_leave(self, _: Event) -> None:
        self._sv_lbl_line_error.set("")

        self._txt_parsed_text.config(cursor=self._default_cursor)

    def _numerate_lines(self, lines: List[str]) -> List[str]:
        digits_for_line_numbers = len(str(len(lines) - 1))
        return [str(index).zfill(digits_for_line_numbers) + " " + line for index, line in enumerate(lines)]
