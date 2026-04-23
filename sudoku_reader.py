"""Module for reading Sudoku boards from text files in different formats.

Currently supports:
- "Compact" format: rows separated by newlines. Includes both puzzle and solution.
- "Oneline" format: entire board in a single line.

In both cases blank spaces are represented by zeros or non-digit characters.

Functions
---------
read_sudoku_boards(file_path: str | Path) -> list[tuple[list[list[int]], list[list[int]]]]:
    Read multiple Sudoku boards with solutions from a file in "compact" format.

sudoku_board_generator_oneline(file_path: str | Path):
    Generator that yields Sudoku boards saved to a file in "oneline" format .

sudoku_compact_to_int_list(board_str: str) -> list[list[int]]:
    Convert Sudoku board saved in "compact" format to nested list of integers.

sudoku_oneline_to_int_list(board_str: str) -> list[list[int]]:
    Convert Sudoku board saved in "oneline" format to nested list of integers.

Example "compact" format (single board, not showing solution):
    ......7..
    ....7.3.5
    .......96
    ..8.5.4..
    ........8
    .4..932..
    75.94....
    8....7..2
    6.2.8.5.4

Example "oneline" format:
    004300209005009001070060043006002087190007400050083000600000105003508690042910300

"""

from math import isqrt
from pathlib import Path


def sudoku_compact_to_int_list(board_str: str) -> list[list[int]]:
    """Convert Sudoku board saved in "compact" format to nested list of integers

    Parameters
    ----------
    board_str : str
        Sudoku board in compact text format, with rows separated by newlines. Blank spaces
        are represented by zeros or by non-digit characters (e.g., periods).

    Returns
    -------
    list[list[int]]
        List of rows, with blank spaces represented as 0.

    Examples
    --------
    >>> board_str = ".423\n.31.\n.13.\n3..."
    >>> sudoku_compact_to_int_list(board_str)
    [[0, 4, 2, 3], [0, 3, 1, 0], [0, 1, 3, 0], [3, 0, 0, 0]]
    """
    sudoku_board = []
    for row in board_str.split("\n"):
        sudoku_board.append(
            [(int(char) if char.isdigit() else 0) for char in row.strip()]
        )
    return sudoku_board


def sudoku_oneline_to_int_list(board_str: str) -> list[list[int]]:
    """Convert sudoku board in "oneline" text format to nested list of integers

    Parameters
    ----------
    board_str : str
        Sudoku board in oneline text format, with blank spaces represented by zero or
        by non-digit characters (e.g., periods).

    Returns
    -------
    list[list[int]]
        List of rows, with blank spaces represented as 0.

    Examples
    --------
    >>> board_str = "0423031001303000"
    >>> sudoku_oneline_to_int_list(board_str)
    [[0, 4, 2, 3], [0, 3, 1, 0], [0, 1, 3, 0], [3, 0, 0, 0]]
    """
    side_length = isqrt(len(board_str))
    sudoku_board = []
    for i in range(side_length):
        row = board_str[i * side_length : (i + 1) * side_length]
        sudoku_board.append([(int(char) if char.isdigit() else 0) for char in row])
    return sudoku_board


def read_sudoku_boards(
    file_path: str | Path,
) -> list[tuple[list[list[int]], list[list[int]]]]:
    """Read multiple Sudoku boards with solutions, saved in "compact" format, from a file.

    Parameters
    ----------
    file_path : str | Path
        Path to the file containing Sudoku boards.

    Returns
    -------
    list[tuple[list[list[int]], list[list[int]]]]
        List of tuples, where each tuple contains a puzzle board and its corresponding
        solution board.

    Notes
    -----
    The puzzle and the solution should be separated by a blank line. Each (puzzle,
    solution) pair should be separated from the next by *two* blank lines.
    """
    # Read file
    with open(file_path, "r") as file:
        file_contents = file.read().strip()  # Remove leading/trailing whitespace

    # Split into individual boards (with solutions)
    board_strings = file_contents.split("\n\n\n")  # Three newlines -> two blank lines

    # Parse each board string into puzzle and solution
    puzzle_solution_pairs = []
    for board_str in board_strings:
        puzzle_str, solution_str = board_str.split("\n\n")
        puzzle = sudoku_compact_to_int_list(puzzle_str)
        solution = sudoku_compact_to_int_list(solution_str)
        puzzle_solution_pairs.append((puzzle, solution))

    return puzzle_solution_pairs


def sudoku_board_generator_oneline(file_path: str | Path):
    """Generator that yields Sudoku boards from a file in "oneline" format.

    Parameters
    ----------
    file_path : str | Path
        Path to the file containing Sudoku boards in oneline format.

    Yields
    ------
    list[list[int]]
        Sudoku board as a nested list of integers.
    """
    with open(file_path, "r") as file:
        for line in file:
            board_str = line.strip()
            if board_str:  # Skip any empty lines
                yield sudoku_oneline_to_int_list(board_str)


if __name__ == "__main__":
    """Test reading Sudoku boards (if run as main module)"""

    print("\nReading 4x4 Sudoku boards in compact (matrix) format:\n")
    example_file_compact_format = Path(r"sudoku_datafiles/4x4.txt")
    boards = read_sudoku_boards(example_file_compact_format)
    for puzzle, solution in boards:
        print("Puzzle:")
        for row in puzzle:
            print(row)
        print("Solution:")
        for row in solution:
            print(row)
        print()

    print("Reading Sudoku boards in oneline format:\n")
    example_file_online_format = Path(r"sudoku_datafiles/4x4.txt")
    for board in sudoku_board_generator_oneline(example_file_online_format):
        print("Board:")
        for row in board:
            print(row)
        print()
