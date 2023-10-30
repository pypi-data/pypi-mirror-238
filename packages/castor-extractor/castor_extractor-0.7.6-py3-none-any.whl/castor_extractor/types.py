"""convert files to csv"""
from typing import Literal, TypedDict


class CsvOptions(TypedDict):
    delimiter: str
    quoting: Literal[1]
    quotechar: str
    escapechar: str
