from abc import ABC, abstractmethod
from typing import List

class BaseFilter(ABC):
    @abstractmethod
    def apply_filter(self, words: List[str]) -> List[str]:
        pass