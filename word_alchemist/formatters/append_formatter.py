from .base_formatter import BaseFormatter
from typing import List

class AppendFormatter(BaseFormatter):
    """
        Formatter that appends a string to all permutations.
    """
    def __init__(self, append_word: str):
        self.append_word = append_word

    def apply_formatter(self, results: List[str]):
        return [result + ' ' + self.append_word for result in results]