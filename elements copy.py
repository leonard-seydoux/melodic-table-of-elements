"""Utility functions for working periodid tables of elements."""

import pandas as pd


MAIN_TABLE_ROWS = 7
MAIN_TABLE_COLS = 18
SUB_TABLE_ROWS = 2
SUB_TABLE_COLS = 14


def read_elements_from_csv(filename):
    """Read the periodic table of elements from a CSV file."""
    elements = pd.read_csv(filename, delimiter=",", encoding="unicode_escape")
    return elements


if __name__ == "__main__":

    # Read the periodic table of elements
    elements = read_elements_from_csv("periodic-table.csv")
    print(elements)
