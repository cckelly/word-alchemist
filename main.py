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
# add comments where necessary
# use typing
# confirm file structure

def parse_args() -> argparse.Namespace:
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

def get_formatters(args: List[str]) -> List[str]:
    formatters = []
    if args.join:
        formatters.append(JoinFormatter())

    if args.append:
        formatters.append(AppendFormatter(args.append))

    if args.capitalize:
        formatters.append(CapitalizeFormatter())

    return formatters

def handle_results(results: List[str], output_file: str):
    if output_file:
        if output_file:
            with open(output_file, 'w') as out:
                out.writelines(result + '\n' for result in results)
    else:
        for result in results:
            print(result)

def main():
    args = parse_args()
    formatters = get_formatters(args)

    alchemist = WordAlchemist(
        args.files, 
        args.filters, 
        formatters, 
        args.first_word, 
        args.second_word
    )

    # just to be cute
    results = alchemist.mix()
    if len(results) == 0:
        print("No results found")
        return

    handle_results(results, args.output)

if __name__ == '__main__':
    main()