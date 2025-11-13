# Python Word Search Tool

**Author:** Zoë Finelli  
**Course:** A.B. Cognitive Science - CSCI1300  
**Date:** 08 December 2024

---

A command-line application for generating and solving word search puzzles, written in Python and designed following object-oriented principles.

## Overview

This project serves as a comprehensive tool for both creating new word search puzzles and solving existing ones. It emphasizes modern practices in Python software development, including strong encapsulation through object-oriented programming (OOP), robust file handling, and a clear, professional command-line interface.

The tool supports advanced puzzle generation logic such as diagonal word placement, overlapping words, and customization of puzzle dimensions. It is well-suited both for casual users and for those interested in the underlying algorithms of grid-based puzzle creation and search.

## Features

- **Dual functionality:** The program can either generate new puzzles from a word list or solve existing puzzles using a specified word bank.
- **Eight-directional word placement:** Words may be placed horizontally, vertically, and diagonally in both directions, providing a high level of puzzle complexity.
- **Support for overlapping words:** The generator intelligently allows words to share letters, increasing density while ensuring correctness.
- **Flexible file input and output:** Accepts plain text files for both word lists and puzzle grids, and produces outputs including puzzles, answer keys, and detailed solution reports.
- **Human-readable and machine-parseable outputs:** Solver results are written to a JSON file specifying found words, their coordinates, and directions; answer keys can be generated for manual review.
- **Command-line interface:** All features are accessible via clear command-line arguments with the help of Python’s `argparse` module.
- **Graceful error handling:** Handles missing files and infeasible word placements appropriately, with meaningful feedback.

## Usage

### Prerequisities
- Python 3.10+: This script is written using modern Python (like pathlib and argparse), so a recent version is recommended.

- No external libraries needed. All modules used (random, json, sys, argparse, pathlib) are part of the Python Standard Library. This means you don't need to pip install anything. It's ready to run right away.

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/znfinelli/python-word-search-tool.git
    cd python-word-search-tool
    ```

### Generating a New Puzzle

To generate a puzzle, use the `generate` mode. Specify a word list, the number of rows, and the number of columns:

```bash
python word_search_tool.py generate -w wordBank.txt -r 15 -c 15
```

By default, this creates two files:
- `wordPuzzle_new.txt` — The completed puzzle, filled with random letters except where words are placed.
- `wordPuzzle_key.txt` — An answer key showing only the locations of placed words.

### Solving an Existing Puzzle

To solve a puzzle and locate specified words within a grid, use the `solve` mode:

```bash
python word_search_tool.py solve -p testPuzzle.txt -w testBank.txt
```

This command produces:
- `wordSearchResults.json` — A structured solution detailing each found word, including its grid coordinates and direction.

To create a human-readable answer key showing the locations of found words, add the `--ok` argument:

```bash
python word_search_tool.py solve -p testPuzzle.txt -w testBank.txt --ok my_solved_key.txt
```

## Program Design and Algorithmic Details

The core of this tool is encapsulated in the `WordSearch` class, which maintains all relevant state and ensures clear separation of responsibilities. This design approach guarantees that puzzle grids and word lists are managed safely, avoiding global state and facilitating future extensibility.

### Directional Placement

The program uses a dictionary of "direction vectors" to represent all valid placement directions in the grid:

```python
self.directions = {
    'forward': (0, 1),
    'backward': (0, -1),
    'down': (1, 0),
    'up': (-1, 0),
    'diag_fd': (1, 1),
    'diag_bd': (1, -1),
    'diag_fu': (-1, 1),
    'diag_bu': (-1, -1)
}
```

This abstraction allows all word placement and search operations to use a single generalized algorithm, making the code concise, less error-prone, and easier to maintain.

### Handling Overlaps and Grid Constraints

During word placement, the generator verifies both grid boundaries and compatibility with already-placed letters. Overlapping is permitted only if the intersecting grid cell contains the same letter as required by the new word. This enables the creation of dense, realistic puzzles where words may cross, and ensures every puzzle remains solvable and correct.

### Example Outputs

#### Solver Output (`wordSearchResults.json`):

```json
{
    "is": {
        "direction": "forward",
        "start": [
            0,
            2
        ],
        "end": [
            0,
            3
        ]
    },
    "test": {
        "direction": "forward",
        "start": [
            1,
            2
        ],
        "end": [
            1,
            5
        ]
    },
    "this": {
        "direction": "backward",
        "start": [
            3,
            9
        ],
        "end": [
            3,
            6
        ]
    },
    "search": {
        "direction": "forward",
        "start": [
            4,
            4
        ],
        "end": [
            4,
            9
        ]
    },
    "the": {
        "direction": "diag_bu",
        "start": [
            6,
            2
        ],
        "end": [
            4,
            0
        ]
    },
    "most": {
        "direction": "diag_bu",
        "start": [
            6,
            6
        ],
        "end": [
            3,
            3
        ]
    },
    "word": {
        "direction": "diag_bd",
        "start": [
            6,
            8
        ],
        "end": [
            9,
            5
        ]
    },
    "ultimate": {
        "direction": "up",
        "start": [
            9,
            3
        ],
        "end": [
            2,
            3
        ]
    }
}
```

#### Visual Key Output (`my_solved_key.txt`):

An answer key grid showing only the positions of found words; all other spaces are marked with asterisks.

```
* * i s * * * * * *
* * t e s t * * * *
* * * e * * * * * *
* * * t * * s i h t
e * * a s e a r c h
* h * m * o * * * *
* * t i * * m * w *
* * * t * * * o * *
* * * l * * r * * *
* * * u * d * * * *
```

## Learning Outcomes

Working on this project developed stronger skills in object-oriented design, grid-based algorithms, and user-oriented interface development. I learned to refactor procedural code into organized classes, create scalable solutions for 2D search problems, and adopt modern Python tools—such as `pathlib` for file operations and `argparse` for comprehensive CLI interfaces.
