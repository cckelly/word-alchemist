from abc import ABC, abstractmethod
from typing import List

class BaseFormatter(ABC):
    @abstractmethod
    def apply_formatter(self, results: List[str]) -> List[str]:
        pass