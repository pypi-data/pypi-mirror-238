import pytest

from northpole.parsers import int_list_parser, parse_string


def test_int_list_parser() -> None:
    data: str = "1x3\n6x2"
    split_on: str = "x"
    expected: list[list[int]] = [[1, 3], [6, 2]]

    parser = int_list_parser(split_on)
    
    assert parser(data) == expected


@pytest.mark.parametrize("expected,suffix", [("Santa", "\n"), ("Santa", "\nClause"), ("Santa", "")])
def test_parse_string(expected: str, suffix: str) -> None:
    data: str = f"{expected}{suffix}"

    assert parse_string(data) == expected
