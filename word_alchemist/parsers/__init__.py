"""
    Contains all parsers, any class that operates on
    input from the CLI to prepare it for processing.
"""
from .filter_parser import FilterParser
from .json_parser import JsonParser

__all__ = [
    "FilterParser",
    "JsonParser",
]