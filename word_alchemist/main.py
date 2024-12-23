from word_alchemist import WordAlchemist
from word_alchemist.formatters import *
from word_alchemist.filters import *
from typing import List
import argparse

def parse_args() -> argparse.Namespace:
    """
        Parses CLI args into a usable Namespace object
    """
    parser = argparse.ArgumentParser(
        description="Simple Python CLI to help you brainstorm the name of your next product, studio, brand etc"
    )
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help="[Required] List of JSON files containing words to permutate"
    )
    parser.add_argument(
        '-fw',
        '--first-word',
        default='',
        help="[Optional] Becomes the default first word in all permutations"
    )
    parser.add_argument(
        '-sw',
        '--second-word',
        default='',
        help="[Optional] Becomes the default second-word in all permutations"
    )
    parser.add_argument(
        '--filters',
        nargs='+',
        default=[],
        help="Filters to use on the JSON files above, see the documentation for examples"
    )
    parser.add_argument(
        '-j',
        '--join',
        action='store_true',
        help="[Optional] Join words together, removing spaces"
    )
    parser.add_argument(
        '-c',
        '--capitalize',
        action='store_true',
        help='[Optional] Capitalize first letter of each word in the output'
    )
    parser.add_argument(
        '-a',
        '--append',
        default='',
        help='[Optional] String to append to all permutations'
    )
    parser.add_argument(
        '-o',
        '--output',
        default='',
        help="[Optional] Output file to log results to, otherwise will be printed"
    )
    return parser.parse_args()

def get_formatters(args: List[str]) -> List[str]:
    """
        Reads formatter flags and converts them to formatters to use.
    """
    formatters = []

    # this order is opinionated about the typical results a user wants
    # can always customize this order via the CLI if desired in the future

    if args.join:
        formatters.append(JoinFormatter())

    if args.append:
        formatters.append(AppendFormatter(args.append))

    if args.capitalize:
        formatters.append(CapitalizeFormatter())

    return formatters

def handle_results(results: List[str], output_file: str):
    """
        Outputs final permutations to either a 
        file or prints to the log depending on input.
    """
    if output_file:
        if output_file:
            with open(output_file, 'w') as out:
                out.writelines(result + '\n' for result in results)
    else:
        for result in results:
            print(result)

def main():
    """
        Main entry point
    """
    args = parse_args()
    formatters = get_formatters(args)

    alchemist = WordAlchemist(
        args.files, 
        args.filters, 
        formatters, 
        args.first_word, 
        args.second_word
    )

    results = alchemist.mix()
    if len(results) == 0:
        print("No results found")
        return

    handle_results(results, args.output)

if __name__ == '__main__':
    main()