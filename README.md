🐍 Python Word Search Tool

This is a command-line tool written in Python that can both generate new word search puzzles and solve existing ones.

I built this project to practice my Python skills, specifically focusing on Object-Oriented Programming (OOP), file I/O, and creating a clean, professional command-line interface. It's a big step up from my first script-based projects!

✨ Key Features

Dual Modes: Works as both a puzzle Generator and a puzzle Solver.

Complex Generation: The generator intelligently places words in all 8 directions (horizontal, vertical, and diagonal).

Smart Overlap: Words can share letters, allowing for complex and dense puzzles, just like real ones.

Flexible I/O: Reads from simple .txt files for both grids and word banks.

Detailed Output: The solver outputs a .json file with the coordinates and direction of every word, and can generate a human-readable .txt answer key.

CLI Interface: Uses Python's argparse module for a professional command-line experience (no more messy input() prompts!).

🚀 How to Use

First, clone this repository to your local machine:

git clone [https://github.com/your-username/python-word-search-tool.git](https://github.com/your-username/python-word-search-tool.git)
cd python-word-search-tool


The script word_search_tool.py has two main commands: generate and solve.

1. To Generate a New Puzzle

Use the generate command. You must provide a word list (-w), the number of rows (-r), and the number of columns (-c).

# Example: Generate a 15x15 puzzle using words from 'wordBank.txt'
python word_search_tool.py generate -w wordBank.txt -r 15 -c 15


This will create two files:

wordPuzzle_new.txt: The final puzzle, filled with random letters.

wordPuzzle_key.txt: The answer key, showing only the placed words.

2. To Solve an Existing Puzzle

Use the solve command. You must provide the puzzle file (-p) and a word list (-w).

# Example: Solve 'testPuzzle.txt' using words from 'testBank.txt'
python word_search_tool.py solve -p testPuzzle.txt -w testBank.txt


This command will create wordSearchResults.json.

✨ (Optional) Get a .txt Answer Key from the Solver

I also added a feature to get a visual answer key. Just add the --ok (output key) argument:

# This does the same as above, but ALSO creates 'my_solved_key.txt'
python word_search_tool.py solve -p testPuzzle.txt -w testBank.txt --ok my_solved_key.txt


🎓 Project Design & What I Learned

This project was a fantastic learning experience in software design.

Object-Oriented Design: The biggest goal was to avoid global variables. I refactored my entire original script into a single WordSearch class. All the data (like the grid and word list) is stored as self attributes. This makes the code much cleaner, safer, and easier to debug.

Algorithmic Thinking (The 8 Directions): My favorite part. Instead of writing 8 huge if/elif blocks for each direction, I used a dictionary of "direction vectors":

self.directions = {
    'forward': (0, 1),  # (row_change, col_change)
    'up':      (-1, 0),
    'diag_fd': (1, 1),
    ...etc
}


Now, I have one function for placing/checking words that just iterates over these vectors. This was a breakthrough for me and felt like a much smarter, more scalable way to handle complex 2D grid logic—something that will be really useful in my future AI and robotics courses.

Clean File Handling: I used pathlib for modern path management and argparse to build a real CLI tool. This taught me how to make a script that other people (or even my future self) can use easily without having to read all the code.

📁 Example Outputs

wordSearchResults.json (Solver Output)

{
    "this": {
        "direction": "backward",
        "start": [
            3,
            8
        ],
        "end": [
            3,
            5
        ]
    },
    "test": {
        "direction": "forward",
        "start": [
            1,
            3
        ],
        "end": [
            1,
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
    "ultimatest": {
        "coordinates": "word not found"
    }
}


my_solved_key.txt (Optional Solver Output)

* * * * * * * * * * * * * t e s t * * * * * * * * * * * * * * * * * * t h i s 
* * * * s e a r c h 
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ```

---

### 📝 License

This project is open-source and available under the [MIT License](LICENSE).
