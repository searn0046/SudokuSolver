# SudokuSolver

INF-1400 Mandatory Assignment 1 (Sudoku Solver).

This project implements a Sudoku solver with support for 4x4, 6x6, and 9x9 boards,
including a test suite using `pytest`.

## Features

- Solves Sudoku puzzles using recursive backtracking.
- Supports multiple board sizes:
	- 4x4 (2x2 boxes)
	- 6x6 (3x2 boxes)
	- 9x9 (3x3 boxes)
- Includes input parsing utilities for Sudoku board files.
- Includes unit tests for initialization, validation, and solving behavior.

## Project Structure

- `main.py`: Core Sudoku classes and solver logic, plus runnable demo.
- `sudoku_reader.py`: Utility functions for reading/parsing Sudoku boards from files.
- `test_main.py`: `pytest` test suite.
- `requirements.txt`: Python dependencies (`pytest`).
- `sudoku_datafiles/`: Example Sudoku boards used by the solver.

## Prerequisites

- Python 3.10+ (recommended: latest Python 3 version available on your system)
- `pip` (Python package installer)

## Setup

Run all commands from the project root (the folder containing `main.py`).

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

If script execution is blocked in PowerShell, run this first (current terminal only):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then run:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)

```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the Program

### macOS / Linux

```bash
python3 main.py
```

### Windows

```powershell
python main.py
```

The program will load example boards from `sudoku_datafiles/` and print puzzle/solution pairs.

## Run Tests (pytest)

Make sure the virtual environment is activated and dependencies are installed.

### macOS / Linux

```bash
pytest
```

### Windows

```powershell
pytest
```

Optional verbose output:

```bash
pytest -v
```

## Deactivate Virtual Environment

When finished:

```bash
deactivate
```

## Notes

- Keep `.venv/` out of version control (already covered by typical `.gitignore` setups).
- If `pytest` is not found, ensure the virtual environment is activated and reinstall dependencies:

```bash
python -m pip install -r requirements.txt
```
