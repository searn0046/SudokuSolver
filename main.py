from abc import ABC, abstractmethod
import sudoku_reader as reader
from pathlib import Path
from time import sleep
import math

class Sudoku(ABC):
    # Generic (abstract) representation of Sudoku board.

    def __init__(self, initial_board: list[list[int]],
                box_width: int, box_height: int):

        self.initial_board = initial_board
        self.box_width = box_width
        self.box_height = box_height
        self.total_sq_qty = sum(len(row) for row in self.initial_board)
        self.max_value = math.sqrt(int(self.total_sq_qty)) # This is also its side length

        self._validate_board_dimensions() # Also turns 'self.max_value' into an int.
       
        self.box_row_qty = self.max_value // self.box_height    # For 6x6 to work.
        self.box_column_qty = self.max_value // self.box_width
        self.box_qty = self.box_row_qty * self.box_column_qty

        self.squares = []
        self.elements = []
        self._set_up_board()
        self._validate_board_values()

    def _validate_board_dimensions(self):
        # Validating dimensions of initial board.

        if not (
            (self.max_value.is_integer() == True)          # The board is a square.
            and (self.max_value > 0)                       # It actually has squares.
            and (self.max_value % self.box_width == 0)     # The boxes fit both horizontally
            and (self.max_value % self.box_height == 0)    # and vertically on the board.
        ):
            raise ValueError(f"Invalid board dimensions:\
                            \nBoxes are {self.box_width} X {self.box_height}.")
        else:
            self.max_value = int(self.max_value)

    def _set_up_board(self):
        # Initializing Square and Element objects.

        self.rows = []
        for some_row in range(self.max_value):  # 0-8 (9 in total)
            self.rows.append(Row())
        self.elements.append(self.rows)

        self.columns = []
        for some_column in range(self.max_value):
            self.columns.append(Column())
        self.elements.append(self.columns)

        self.boxes = []
        for some_box in range(1, self.box_qty + 1):
            self.boxes.append(Box(self.box_width, self.box_height))
        self.elements.append(self.boxes)

        for row_index in range(self.max_value):
            single_row = []
            for column_index in range(self.max_value):
                single_row.append(None) # Empty placeholders for Square objects.
            self.squares.append(single_row)

        # Creating all the Square objects.
        for row in range(self.max_value):
            for column in range(self.max_value):
                box_row = row // self.box_height
                box_column = column // self.box_width
               
                # Calculating box index of each square. I need a new brain after this.
                box_index = int(box_row) * int(self.box_column_qty) + int(box_column)
                value = self.initial_board[row][column]
                sqr = Square(value,
                            self.max_value,
                            self.rows[row],
                            self.columns[column],
                            self.boxes[box_index])
                self.squares[row][column] = sqr

    def _validate_board_values(self):
        # Validating the values of the board:
        # - No duplicate values in any row, column, or box.
        # - All values are within the valid range.

        for row in range(self.max_value):
            for column in range(self.max_value):    # 0 means unfilled square.
                if not (self.initial_board[row][column] in range(0, self.max_value + 1)):
                    raise ValueError(f"The board contains value(s) outside the valid range (0, {self.max_value + 1}):\
                    \n\x1b[5m{self.initial_board[row][column]}\x1b[0m")
        
        # Isolating the non-zero values, since 0 can be repeated.
        for el_group in range(len(self.elements)):
            for element in self.elements[el_group]:
                element_values = element.values()
                vals = []
                for val in element_values:
                    if val != 0:
                        vals.append(val)

                # Comparing the list to the 'set' version of itself (no duplicates)
                if len(vals) != len(set(vals)):
                    raise ValueError("A number exists more than once in the same row/column/box.")

    def recursively_solved(self):
        for row in self.squares:
            for square in row:
                if square.value == 0:   # AKA an unfilled square.
                    possibilities = square.possible_values()
                    for poss_value in possibilities:
                        square.value = poss_value
                        if self.recursively_solved():
                            return True # All good, proceed.
                        else:
                            square.value = 0 # Nope. Backtracking...
                    return False
        return True # When all squares are filled in.

    def solve(self) -> list[list[int]] | None:
        # Solving Sudoku and returning board with all values filled in.

        if self.recursively_solved(): # 'True' if solved.
            solved_board = []
            for row in range(self.max_value):
                solved_row = []
                for column in range(self.max_value):
                    solved_row.append(self.squares[row][column].value)
                solved_board.append(solved_row)
            return solved_board # Another nested list.
        else:
            print("No solution.\n")
            return None
            
    def __str__(self) -> str:
        # Returning a string representation of the Sudoku board.

        display_board = []
        self.h_border_length = 0

        j = 1
        for row in self.initial_board:
            # Multiplying by 3 to account for the spaces around the numbers.
            self.h_border_length = (self.box_width * self.box_height * j * 3)
            i = 0
            for square in row:
                if i % self.box_width == 0 and 0 < i < self.max_value:
                    display_board.append('\x1b[2m|\x1b[0;1m')
                if square == 0:
                    display_board.append(' \x1b[0;2m?\x1b[0;1m ')
                else:
                    display_board.append(f" {square} ")
                i += 1
            j += 1
            display_board.append('\n')

            if (j - 1) % self.box_height == 0 and j < self.max_value:
                display_board.append(" \x1b[2m" + ('-' * (self.h_border_length // (j - 1))) + "\x1b[0;1m\n")
            elif j <= self.max_value:
                v_border_space = str(' ' * ((self.h_border_length // (j - 1)) // (self.max_value // self.box_width)))
                display_board.append('\x1b[2m|\x1b[0;1m'.join([v_border_space] * self.box_column_qty))
                display_board.append('\n')
            if (j - 1) % self.box_height == 0:
                display_board.append('\x1b[0;1m')

        display_board_str = ''.join(str(piece) for piece in display_board)
                
        return display_board_str

class Sudoku_4x4(Sudoku):
    def __init__(self, initial_board):
        super().__init__(initial_board, 2, 2)

class Sudoku_6x6(Sudoku):
    def __init__(self, initial_board):
        super().__init__(initial_board, 3, 2)

class Sudoku_9x9(Sudoku):
    def __init__(self, initial_board):
        super().__init__(initial_board, 3, 3)

class Square:
    # A single square of a Sudoku board
    def __init__(self, value: int, max_value: int, row: "Row",
        column: "Column", box: "Box"):

        self.value = value
        self.max_value = max_value
        self.row = row
        self.column = column
        self.box = box
        self.elements = [self.row, self.column, self.box]

        # Adding this square to its elements
        self.row.add_square(self)
        self.column.add_square(self)
        self.box.add_square(self)

    def possible_values(self) -> list[int]:
        # Returning list of possible values by process of elimination
        possibilities = list(range(1, self.max_value + 1))
        for element in self.elements:
            for value in element.values():
                if value in possibilities:
                    possibilities.remove(value)

        return possibilities

    def __str__(self):  # Used mainly for testing. Not strictly necessary.
        return f"{self.value}"

class Element(ABC):
    # Generic Sudoku element containing a collection of squares
    def __init__(self):
        self.squares = []   # Not to be confused with the Sudoku object's squares.

    def add_square(self, square: Square) -> None:
        # To be called by Square().__init__()
        self.squares.append(square)

    def values(self) -> list[int]:
        # Returning values of squares that have been filled in 
        # (To be called by Square.possible_values())
        values = []
        for square in self.squares:
            if square.value in range(1, square.max_value + 1):
                values.append(square.value)
        return values

    @abstractmethod  # Implemented by subclasses
    def __str__(self) -> str:
        pass

class Row(Element):
    def __str__(self):
        row_string = []
        for square in self.squares:
            row_string.append(str(square.value))
        return " ".join(row_string)

class Column(Element):

    def __str__(self):
        # Converting each value to a string (0 becomes '?')
        column_string = []
        for square in self.squares:
                column_string.append(str(square.value))
        return "\n".join(column_string)
        # Can be used for testing, but not strictly necessary.
    
class Box(Element):
    def __init__(self, box_width, box_height):
        super().__init__()
        self.box_width = box_width
        self.box_height = box_height

    def __str__(self):
        box_string = []

        for i in range(0, len(self.squares), self.box_width):            
            current_row_chunk = self.squares[i : i + self.box_width]
            row_str = []
            for square in current_row_chunk:
                row_str.append(str(square.value))
            
            box_string.append(" ".join(row_str) + "\n")

        return "".join(box_string)

def solve_boards(file_path, max_num_of_boards, cool_mode: bool, dimensions: str):
    print(f"\n\n \x1b[1;36m{dimensions.upper()} SUDOKU\x1b[0;1m\n")
    sleep(0.25)

    puzz_and_sol = reader.read_sudoku_boards(file_path)
    puzzles = []
    for sudoku_tuple in puzz_and_sol:   # Extracting only puzzles from
        puzzles.append(sudoku_tuple[0]) # tuples of puzzles & solutions.

    for i in range(max_num_of_boards):
        
        puzzle = puzzles[i]
        if dimensions.upper() == "4X4":
            unsolved_board = Sudoku_4x4(puzzle)
        elif dimensions.upper() == "6X6":
            unsolved_board = Sudoku_6x6(puzzle)
        elif dimensions.upper() == "9X9":
            unsolved_board = Sudoku_9x9(puzzle)
        else:
            raise ValueError("Invalid board dimensions specified.")
            return
        
        print(f"\n\n \x1b[1;4mPuzzle {i + 1}\x1b[0;1m\n")
        print(unsolved_board, "\n \x1b[0mThinking", end = "", flush = True)
        if cool_mode == True:
            for _ in range(3):
                print(".", end = "", flush = True)
                sleep(0.2)
        else:
            print("...", end = "")
        print("\n")

        solution = unsolved_board.solve()
        if isinstance(unsolved_board, Sudoku_4x4):
            solved_board = Sudoku_4x4(solution)
        elif isinstance(unsolved_board, Sudoku_6x6):
            solved_board = Sudoku_6x6(solution)
        elif isinstance(unsolved_board, Sudoku_9x9):
            solved_board = Sudoku_9x9(solution)
        
        print(f" \x1b[1;4mSolution\x1b[0;1m\n")
        if cool_mode == True:   # A "cool" illusion, giving some LLM vibes.
            for character in list(str(solved_board)):
                print(str(character), end = "", flush = True)
                sleep(1 / (len(str(solved_board) * 2)))
        else:
            print(solved_board)
        sleep(0.5)
        print()

        if i >= len(puzzles) - 1:
            return

if __name__ == "__main__":

    print("\x1b[H\x1b[2J\x1b[3J", end = "") # Clearing the terminal
    print("\n \x1b[0;5;35m-------------------\
        \n|                   |\
        \n|   \x1b[1;3;5;36mSUDOKU SOLVER\x1b[0;5;35m   |\
        \n|                   |\
        \n -------------------\x1b[0m\n")
    sleep(1)

    solve_boards(Path(r"sudoku_datafiles/4x4.txt"),
                max_num_of_boards = 5,
                cool_mode = True,
                dimensions = "4X4")

    print("\x1b[0;35m_" * 16,
        "\x1b[1;36m_\x1b[0m" * 17,
        "\x1b[0;35m_\x1b[0m" * 18,
        sep = "\n")
                
    solve_boards(Path(r"sudoku_datafiles/6x6.txt"),
                max_num_of_boards = 3,
                cool_mode = True,
                dimensions = "6X6")

    print("\x1b[0;35m_" * 24,
        "\x1b[1;36m_\x1b[0m" * 26,
        "\x1b[0;35m_\x1b[0m" * 28,
        sep = "\n")

    solve_boards(Path(r"sudoku_datafiles/9x9.txt"),
                max_num_of_boards = 6,
                cool_mode = True,
                dimensions = "9X9")