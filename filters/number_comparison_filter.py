from .base_filter import BaseFilter
from typing import Callable, List
import operator

operator_map = {
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt
}

class NumberComparisonFilter(BaseFilter):
    def __init__(self, get_count: Callable[[str], int], operator_symbol: str, target: int):
        self.get_count = get_count
        self.operator = operator_map.get(operator_symbol)
        self.target = target

    def apply_filter(self, words: List[str]) -> List[str]:
        return [word for word in words if self.operator(self.get_count(word), self.target)]