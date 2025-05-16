import pytest
from process_raw_data import (
    remove_information_in_brackets, desc_order, clean_data)


@pytest.mark.parametrize("a,b", [
    ("The Book Title(Second Edition)", "The Book Title"),
    ("Title (Note) Extra", "Title  Extra"),
    ("No Brackets Here", "No Brackets Here"),
    ("(Only Brackets)", "")
])
def test_remove_information_in_brackets(a, b):
    assert remove_information_in_brackets(a) == b


def test_desc_order():
    sample_data = [
        ["Book 1", "Sara", 2000, 4.5, 100],
        ["Book 2", "John", 2001, 3.7, 150],
        ["Book 3", "Paul", 1999, 5.0, 200],
    ]

    result = desc_order(sample_data)
    assert result[0][0] == "Book 3"
    assert result[-1][0] == "Book 2"
