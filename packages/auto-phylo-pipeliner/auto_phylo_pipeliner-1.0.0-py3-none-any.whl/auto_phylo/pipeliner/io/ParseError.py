from builtins import Exception
from typing import Dict, List, Optional


class ParseError(Exception):
    def __init__(self, line_errors: Optional[Dict[int, str]] = None, general_errors: Optional[List[str]] = None):
        super().__init__(f"Error parsing text")

        if line_errors is None and general_errors is None:
            raise ValueError("At least one line error or one general error must be provided")

        self._line_errors: Optional[Dict[int, str]] = line_errors
        self._general_errors: Optional[List[str]] = general_errors

    @property
    def line_errors(self) -> Optional[Dict[int, str]]:
        return None if self._line_errors is None else self._line_errors.copy()

    @property
    def general_errors(self) -> Optional[List[str]]:
        return None if self._general_errors is None else self._general_errors.copy()

    @property
    def message(self) -> str:
        message = ""
        if self._general_errors is not None:
            message = "\n - ".join(self._general_errors)

        if self._line_errors is not None:
            message += "\n - ".join(f"Line {line}: {error}" for line, error in self._line_errors.items())

        return message

    def __str__(self):
        if self._line_errors is not None:
            error_lines = list(self._line_errors.keys())
            text = f"Parse error in lines: {error_lines}"

            if self._general_errors is not None:
                text += f" and with {len(self._general_errors)} general errors"
        else:
            text = f"Parse error with {len(self._general_errors)} general errors"  # type: ignore

        return text
