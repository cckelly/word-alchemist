from word_alchemist import WordAlchemist
from formatters import *
from filters import *
from typing import List
import syllapy
import argparse
import sys
import json
import re

# TODO cleanup:
# doc comments on all functions
# full help menu for CLI and arguments
# figure out how to properly package and release a CLI in the python dev env
# output results to a file
# filter matrix compatibility
# add comments where necessary
# use typing
# try/catch

def get_syllable_count(word: str) -> int:
    return syllapy.count(word)

def get_word_length(word: str) -> int:
    return len(word)

filter_map = {
    "length": get_word_length,
    "syllables": get_syllable_count
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--files',
        nargs='+',
        required=True
    )
    parser.add_argument(
        '-fw',
        '--first-word',
        default=''
    )
    parser.add_argument(
        '-sw',
        '--second-word',
        default=''
    )
    parser.add_argument(
        '--filters',
        nargs='+',
        default=[]
    )
    parser.add_argument(
        '-j',
        '--join',
        action='store_true'
    )
    parser.add_argument(
        '-c',
        '--capitalize',
        action='store_true'
    )
    parser.add_argument(
        '-a',
        '--append',
        default=''
    )
    parser.add_argument(
        '-o',
        '--output',
        default=''
    )
    return parser.parse_args()

def filter_words(filename, filter_string):
    words = read_word_json(filename)
    filters = parse_filter_string(filter_string)

    for filter in filters:
        words = filter.apply_filter(words)

    return words

def read_word_json(filename):
    try:
        with open(filename, 'r') as file:
            words = json.load(file)
            if not isinstance(words, list):
                sys.exit(f"File {filename} needs to be a JSON array")
    except FileNotFoundError:
        sys.exit(f"File {filename} not found")
    except json.JSONDecodeError:
        sys.exit(f"File {filename} is not valid JSON")

    return words

def parse_filter_string(filter_string: str) -> List[NumberComparisonFilter]:

    conditions = [condition.strip() for condition in filter_string.split("and")]
    pattern = r"^(length|syllables)\s*(==|!=|>=|<=|>|<)\s*(\d+)$"
    
    filters = []
    attribute_conditions = {}

    for condition in conditions:
        match = re.match(pattern, condition)
        if not match:
            sys.exit(f"Invalid filter condition: {condition}")

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
            sys.exit(f"Unsupported attribute: {attribute}")

    # validate
    for attribute, conditions in attribute_conditions.items():
        validate_conditions(attribute, conditions)

    return filters

def validate_conditions(attribute: str, conditions: List[tuple]):
    equals = [target for op, target in conditions if op == "=="]
    if len(equals) > 1:
        sys.exit(f"Conflicting '==' conditions for {attribute}: {equals}")

    min_value = None
    max_value = None

    for op, target in conditions:
        if op in (">", ">="):
            min_value = max(min_value, target) if min_value is not None else target
        elif op in ("<", "<="):
            max_value = min(max_value, target) if max_value is not None else target

    if min_value is not None and max_value is not None and (min_value > max_value or min_value == max_value):
        sys.exit(
            f"Conflicting range conditions for {attribute}: "
            f"min={min_value}, max={max_value}"
        )

def print_results(results: List[str]):
    for result in results:
        print(result)

def write_results_to_file(output_file: str, results: List[str]):
    with open(output_file, 'w') as file:
        for result in results:
            file.write(result + '\n')

def get_formatters(args: List[str]) -> List[str]:
    formatters = []
    # it's assumed the user wants to always combine then append
    # but can always revisit if we need to customize formatter order
    if args.join:
        formatters.append(JoinFormatter())

    if args.append:
        formatters.append(AppendFormatter(args.append))

    if args.capitalize:
        formatters.append(CapitalizeFormatter())

    return formatters

def main():
    args = parse_args()

    filter_length = len(args.filters)
    file_length = len(args.files)
    if filter_length > file_length:
        sys.exit(f"Cannot have more filters ({filter_length}) than files ({file_length})")

    word_lists = []

    # If first_word is provided, it always goes first
    if args.first_word:
        word_lists.append([args.first_word])
        # If second_word is also provided, it comes immediately after first_word
        if args.second_word:
            word_lists.append([args.second_word])

    # Handle no filters scenario
    if filter_length == 0:
        # Just read all files and add them to word_lists
        for i, filename in enumerate(args.files):
            words = read_word_json(filename)
            word_lists.append(words)

            # If we didn't have a first_word but we do have a second_word,
            # and this is the first file, insert second_word now
            if i == 0 and args.second_word and not args.first_word:
                # Insert second_word right after the first file's words
                word_lists.append([args.second_word])

    else:
        # We have filters. We apply each filter to the corresponding file in order.
        # If we run out of filters but still have files left, we apply the last filter to the remaining files.
        
        # Apply each filter in order to corresponding file
        for i, filter_string in enumerate(args.filters):
            filename = args.files[i]
            filtered_words = filter_words(filename, filter_string)
            word_lists.append(filtered_words)
            
            # If we didn't have a first_word but we do have a second_word,
            # and this is the first file/filter result, insert second_word now.
            if i == 0 and args.second_word and not args.first_word:
                word_lists.append([args.second_word])

        # If there are more files than filters, apply the last filter to the remaining files
        if file_length > filter_length:
            last_filter_string = args.filters[-1]
            for j, filename in enumerate(args.files[filter_length:], start=filter_length):
                filtered_words = filter_words(filename, last_filter_string)
                word_lists.append(filtered_words)
                # If we inserted second_word above (due to first/second word logic),
                # we don't need to repeat. Only insert second_word for the first file if needed.
                # Since by this point, we already handled insertion of second_word (if any)
                # during the first filter application.

    # If after all processing, we have no lists, let the user know
    if len(word_lists) == 0:
        print("No matches found, check your filters")
        return

    # Now permute all collected word lists
    alchemist = WordAlchemist(word_lists)
    results = alchemist.mix()

    # Apply any formatters
    formatters = get_formatters(args)
    for formatter in formatters:
        results = formatter.apply_formatter(results)

    # Output results
    if args.output:
        write_results_to_file(args.output, results)
    else:
        print_results(results)

if __name__ == '__main__':
    main()