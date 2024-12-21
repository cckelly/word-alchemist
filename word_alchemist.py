from formatters.base_formatter import BaseFormatter
from filters import NumberComparisonFilter
from itertools import product
from typing import List
import syllapy
import json
import re

def get_syllable_count(word: str) -> int:
    return syllapy.count(word)

def get_word_length(word: str) -> int:
    return len(word)

filter_map = {
    "length": get_word_length,
    "syllables": get_syllable_count
}

class WordAlchemist():
    def __init__(
        self, 
        files: List[str], 
        filters: List[str],
        formatters: List[BaseFormatter],
        first_word: str,
        second_word: str,
    ):
        self.files = files
        self.filters = filters
        self.formatters = formatters
        self.first_word = first_word
        self.second_word = second_word

    def mix(self) -> List[str]:
        word_lists = self._pour()
        all_combinations = list(product(*word_lists))

        results = []
        for combination in all_combinations:
            results.append(' '.join(combination))

        return results

    def _pour(self) -> List[str]:
        # validate filter length
        filter_length = len(self.filters)
        file_length = len(self.files)
        if filter_length > file_length:
            raise ValueError(
                f"Cannot have more filters ({filter_length}) than files ({file_length})"
            )

        word_lists = []

        # if a first_word is provided, it's always first
        if self.first_word:
            word_lists.append([self.first_word])
            # add second right after if we have one as we can have additional files after
            if self.second_word:
                word_lists.append([self.second_word])

        # handle no filters scenario
        if len(self.filters) == 0:
            # read all files and add them to word_lists
            for i, filename in enumerate(self.files):
                words = self._read_word_json(filename)
                word_lists.append(words)

                # if we didn't have a first_word but have a second_word
                # and this is the first file, add second_word now
                if i == 0 and self.second_word and not self.first_word:
                    word_lists.append([self.second_word])

        else:
            # apply filters in file order, if we have more files than filters we 
            # just apply the last filter to all remaining files below        
            for i, filter_string in enumerate(self.filters):
                filename = self.files[i]
                filtered_words = self._filter_words(filename, filter_string)
                word_lists.append(filtered_words)
    
                if i == 0 and self.second_word and not self.first_word:
                    word_lists.append([self.second_word])

            if file_length > filter_length:
                last_filter_string = self.filters[-1]
                for i, filename in enumerate(self.files[filter_length:], start=filter_length):
                    filtered_words = self._filter_words(filename, last_filter_string)
                    word_lists.append(filtered_words)

        return word_lists
    
    def _parse_filter_string(self, filter_string: str) -> List[NumberComparisonFilter]:

        conditions = [condition.strip() for condition in filter_string.split("and")]
        pattern = r"^(length|syllables)\s*(==|!=|>=|<=|>|<)\s*(\d+)$"
        
        filters = []
        attribute_conditions = {}

        for condition in conditions:
            match = re.match(pattern, condition)
            if not match:
                raise ValueError(f"Invalid filter condition: {condition}")

            attribute, operator_symbol, target = match.groups()
            target = int(target)

            if attribute not in attribute_conditions:
                attribute_conditions[attribute] = []
            attribute_conditions[attribute].append((operator_symbol, target))

            if attribute in filter_map:
                get_count = filter_map[attribute]
                filter = NumberComparisonFilter(get_count, operator_symbol, target)
                filters.append(filter)
            else:
                raise ValueError(f"Unsupported attribute: {attribute}")

        # validate
        for attribute, conditions in attribute_conditions.items():
            self._validate_conditions(attribute, conditions)

        return filters

    def _validate_conditions(self, attribute: str, conditions: List[tuple]):
        equals = [target for op, target in conditions if op == "=="]
        if len(equals) > 1:
            raise ValueError(f"Conflicting '==' conditions for {attribute}: {equals}")

        min_value = None
        max_value = None

        for op, target in conditions:
            if op in (">", ">="):
                min_value = max(min_value, target) if min_value is not None else target
            elif op in ("<", "<="):
                max_value = min(max_value, target) if max_value is not None else target

        if min_value is not None and max_value is not None and (min_value > max_value or min_value == max_value):
            raise ValueError(
                f"Conflicting range conditions for {attribute}: "
                f"min={min_value}, max={max_value}"
            )

    def _filter_words(self, filename: str, filter_string: str):
        words = self._read_word_json(filename)
        filters = self._parse_filter_string(filter_string)

        for filter in filters:
            words = filter.apply_filter(words)

        return words

    def _read_word_json(self, filename: str):
        with open(filename, 'r') as file:
            words = json.load(file)
            if not isinstance(words, list):
                raise ValueError(f"File {filename} needs to be a JSON array")

        return words