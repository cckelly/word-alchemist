from .parsers.filter_parser import FilterParser
from .parsers.json_parser import JsonParser
from .formatters.base_formatter import BaseFormatter
from itertools import product
from typing import List

class WordAlchemist():
    """
        Main logic for taking the files, filters, and generating all permutations.
    """
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
        self.filter_parser = FilterParser()
        self.json_parser = JsonParser()

    def mix(self) -> List[str]:
        word_lists = self._pour()
        all_combinations = list(product(*word_lists))

        results = []
        for combination in all_combinations:
            results.append(' '.join(combination))

        return results

    def _pour(self) -> List[str]:
        # validate filter length, can never have more filters than files
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
                words = self.json_parser.read_word_json(filename)
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
    

    def _filter_words(self, filename: str, filter_string: str):
        words = self.json_parser.read_word_json(filename)
        filters = self.filter_parser.parse_filter_string(filter_string)

        for filter in filters:
            words = filter.apply_filter(words)

        return words

