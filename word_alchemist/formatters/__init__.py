"""
    Contains all text formatters that can 
    be optionally applied to permutations.
"""
from .join_formatter import JoinFormatter
from .append_formatter import AppendFormatter
from .capitalize_formatter import CapitalizeFormatter

__all__ = [
    "JoinFormatter",
    "AppendFormatter",
    "CapitalizeFormatter"
]