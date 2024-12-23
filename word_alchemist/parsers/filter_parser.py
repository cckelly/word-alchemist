from word_alchemist.filters.number_comparison_filter import NumberComparisonFilter
from typing import List
import syllapy
import re

def get_syllable_count(word: str) -> int:
    return syllapy.count(word)

def get_word_length(word: str) -> int:
    return len(word)

filter_map = {
    "length": get_word_length,
    "syllables": get_syllable_count
}

class FilterParser:
    """
        Reads all filters and turns the input string 
        into valid operators to actually filter the words.
    """
    def parse_filter_string(self, filter_string: str) -> List[NumberComparisonFilter]:
        conditions = [condition.strip() for condition in filter_string.split("and")]
        # regex to validate input, a bit coupled at the moment 
        # but with more filters could start to split this out
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

            # build filter list based on conditions found
            if attribute in filter_map:
                get_count = filter_map[attribute]
                filter = NumberComparisonFilter(get_count, operator_symbol, target)
                filters.append(filter)
            else:
                raise ValueError(f"Unsupported attribute: {attribute}")

        # make sure we're using valid number ranges
        for attribute, conditions in attribute_conditions.items():
            self._validate_range_conditions(attribute, conditions)

        return filters

    def _validate_range_conditions(self, attribute: str, conditions: List[tuple]):
        """
            Validate the range conditions by making sure 
            we have a valid number range to operate on
            for things like length and syllables.
        """
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