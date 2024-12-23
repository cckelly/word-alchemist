from .base_formatter import BaseFormatter
from typing import List

class CapitalizeFormatter(BaseFormatter):
    """
        Capitalize the first letter of all words in the output
    """
    def apply_formatter(self, results: List[str]):
        return [result.title() for result in results]