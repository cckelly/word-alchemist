from itertools import product
from typing import List

class WordAlchemist():
    def __init__(self, word_lists: List[List[str]]):
        super().__init__()
        self.word_lists = word_lists

    def mix(self) -> List[str]:
        all_combinations = list(product(*self.word_lists))

        results = []
        for combination in all_combinations:
            results.append(" ".join(combination))

        return results