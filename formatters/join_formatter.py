from .base_formatter import BaseFormatter
from typing import List

class JoinFormatter(BaseFormatter):
    def apply_formatter(self, results: List[str]):
        return [result.replace(' ', '') for result in results]