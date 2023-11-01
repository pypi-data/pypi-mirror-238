from typing import Callable


def int_list_parser(split_on: str) -> Callable:
    """
    Create a parser that will split each line on the provided string, then cast the
    values to ints.

    Args:
        split_on (str): The value to split each line on.
    
    Returns:
        Callable: The parser function to use to parse into a list of lists of ints.
    """
    def parser(data: str) -> list[list[int]]:
        return [[int(x) for x in line.split(split_on)] for line in data.splitlines()]

    return parser


def parse_string(data: str) -> str:
    """
    Parse the input (most likely read from a file) into a single string. The input data
    will be split on new line characters, and the first string will be returned. It
    works on the assumption that while there may be a new line character in the input,
    there is nothing after it.

    Args:
        data (str): The input data to parse.

    Returns:
        str: The string from before the first new line character.
    """
    return data.splitlines()[0]
