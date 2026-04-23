import pytest  # Required, run e.g. 'pip install pytest' to install
#from sudoku_vanilla_solution import (
from main import (
    Box,
    Column,
    Row,
    Square,
    Sudoku_4x4,
    Sudoku_6x6,
    Sudoku_9x9,
)

from sudoku_reader import read_sudoku_boards


def test_init_elements():
    """Test initialization of Rows, Columns, and Boxes"""
    Row()
    Column()
    Box(box_height=3, box_width=3)


def test_init_square():
    """Test initialization of Square"""
    Square(
        value=0,
        max_value=9,
        row=Row(),
        column=Column(),
        box=Box(box_height=3, box_width=3),
    )


def test_init_sudoku_4x4():
    """Test initialization of Sudoku_4x4"""
    board = [[0 for _ in range(4)] for _ in range(4)]  # Empty board
    sudoku = Sudoku_4x4(board)
    assert sudoku.max_value == 4
    assert sudoku.box_height == 2
    assert sudoku.box_width == 2


def test_init_sudoku_6x6():
    """Test initialization of Sudoku_6x6"""
    board = [[0 for _ in range(6)] for _ in range(6)]  # Empty board
    sudoku = Sudoku_6x6(board)
    assert sudoku.max_value == 6
    assert sudoku.box_height == 2
    assert sudoku.box_width == 3


def test_init_sudoku_9x9():
    """Test initialization of Sudoku_9x9"""
    board = [[0 for _ in range(9)] for _ in range(9)]  # Empty board
    sudoku = Sudoku_9x9(board)
    assert sudoku.max_value == 9
    assert sudoku.box_height == 3
    assert sudoku.box_width == 3


def test_sudoku_4x4_invalid_dimensions():
    """Test initialization of Sudoku_4x4 with invalid dimensions"""
    board = [  # Board with invalid dimensions
        [1, 2, 3, 4],
        [3, 4, 1],
        [2, 1, 4, 3],
    ]
    with pytest.raises(ValueError):
        Sudoku_4x4(board)


def test_sudoku_4x4_duplicate_values():
    """Test initialization of Sudoku_4x4 with duplicate values in elements"""
    board = [  # 4x4 board with duplicates
        [2, 0, 0, 1],
        [1, 0, 2, 0],
        [0, 1, 4, 0],
        [1, 2, 1, 0],
    ]
    with pytest.raises(ValueError):
        Sudoku_4x4(board)


def test_sudoku_6x6_invalid_values():
    """Test initialization of Sudoku_6x6 with value outside valid range"""
    board = [  # 6x6 board with duplicates
        [0, 0, 3, 0, 4, 1],
        [0, 1, 4, 5, 0, 0],
        [1, 4, 9, 0, 2, 0],  # 9 is invalid for 6x6 Sudoku
        [0, 0, 2, 0, 6, 0],
        [6, 3, 5, 4, 0, 2],
        [4, 0, 0, 6, 0, 0],
    ]
    with pytest.raises(ValueError):
        Sudoku_6x6(board)


def test_sudoku_4x4_solve_single_square_left():
    """Test solving a 4x4 Sudoku with only one square left to fill"""
    board = [  # 4x4 board with one square left
        [1, 2, 3, 4],
        [3, 4, 1, 2],
        [2, 1, 4, 3],
        [4, 3, 2, 0],  # Only (3,3) is empty
    ]
    expected_board = [  # Expected solved board
        [1, 2, 3, 4],
        [3, 4, 1, 2],
        [2, 1, 4, 3],
        [4, 3, 2, 1],
    ]
    sudoku = Sudoku_4x4(board)
    solved_board = sudoku.solve()

    assert solved_board == expected_board


def test_sudoku_6x6_solve_simple():
    """Test solving a 6x6 Sudoku puzzle with many hints"""
    board = [  # 6x6 board with a simple solution
        [2, 0, 5, 1, 0, 0],
        [0, 3, 4, 2, 5, 6],
        [4, 1, 3, 5, 0, 2],
        [5, 0, 0, 4, 3, 1],
        [0, 0, 2, 0, 1, 4],
        [3, 4, 0, 6, 2, 0],
    ]
    expected_board = [  # Expected solved board
        [2, 6, 5, 1, 4, 3],
        [1, 3, 4, 2, 5, 6],
        [4, 1, 3, 5, 6, 2],
        [5, 2, 6, 4, 3, 1],
        [6, 5, 2, 3, 1, 4],
        [3, 4, 1, 6, 2, 5],
    ]
    sudoku = Sudoku_6x6(board)
    solved_board = sudoku.solve()

    assert solved_board == expected_board


def test_sudoku_9x9_solve_hard():
    """Test solving a hard 9x9 Sudoku puzzle"""
    board = [  # 9x9 board with a hard solution
        [0, 0, 0, 0, 5, 0, 0, 0, 3],
        [0, 0, 0, 0, 7, 1, 2, 0, 5],
        [0, 0, 0, 2, 0, 6, 0, 0, 0],
        [0, 0, 1, 0, 3, 0, 0, 8, 0],
        [8, 0, 0, 0, 0, 5, 3, 0, 0],
        [0, 0, 6, 0, 0, 9, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 7, 3, 2],
        [0, 0, 0, 0, 0, 0, 8, 0, 0],
        [5, 0, 9, 0, 0, 0, 0, 0, 6],
    ]

    expected_board = [  # 9x9 board with a hard solution
        [2, 1, 7, 9, 5, 8, 6, 4, 3],
        [6, 8, 4, 3, 7, 1, 2, 9, 5],
        [9, 3, 5, 2, 4, 6, 1, 7, 8],
        [7, 5, 1, 6, 3, 2, 9, 8, 4],
        [8, 9, 2, 4, 1, 5, 3, 6, 7],
        [3, 4, 6, 7, 8, 9, 5, 2, 1],
        [1, 6, 8, 5, 9, 4, 7, 3, 2],
        [4, 2, 3, 1, 6, 7, 8, 5, 9],
        [5, 7, 9, 8, 2, 3, 4, 1, 6],
    ]

    sudoku = Sudoku_9x9(board)
    solved_board = sudoku.solve()

    assert solved_board == expected_board
