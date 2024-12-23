from .base_formatter import BaseFormatter
from typing import List

class JoinFormatter(BaseFormatter):
    """
        Join (remove whitespace) words together for all permutations 
    """
    def apply_formatter(self, results: List[str]):
        return [result.replace(' ', '') for result in results]