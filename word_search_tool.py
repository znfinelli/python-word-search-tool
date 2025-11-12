"""
Final Project ATRI 4500 – Word Search Puzzle Generator and Solver
Author: Zoë Finelli

This script provides a complete toolset for generating and solving
word search puzzles. It's built using an Object-Oriented (OOP)
design to keep the code organized, reusable, and easy to maintain.

The script can be run from the command line in two modes:
1. 'generate': Creates a new word search puzzle from a word list.
2. 'solve': Finds all words from a word list in an existing puzzle.

Examples:
    python word_search_tool.py generate --words wordBank.txt --rows 10 --cols 10
    python word_search_tool.py solve --puzzle wordPuzzle.txt --words wordBank.txt
"""

import random
import json
import argparse  # Used for creating a professional command-line interface
from pathlib import Path # Modern way to handle file paths
import sys

class WordSearch:
    """
    This class manages all the logic for a word search puzzle.
    By using a class, we can store all the important data
    (like the grid, word list, etc.) as 'self' attributes
    instead of relying on global variables. This keeps the
    state of our puzzle contained and much easier to manage.
    """

    def __init__(self):
        """
        The constructor initializes the 'state' of our puzzle.
        These attributes will be filled in by our other methods.
        """
        self.grid = []
        self.key_grid = []
        self.word_list = []
        self.rows = 0
        self.columns = 0
        
        # This is a key design choice:
        # Instead of writing 8 different functions for each direction
        # (e.g., 'forward', 'up', 'diag_fd'), we can use a dictionary
        # of 'direction vectors'. Each tuple represents the
        # (row_change, col_change) for one step in that direction.
        # This makes the code much cleaner and follows the DRY
        # (Don't Repeat Yourself) principle.
        self.directions = {
            'forward': (0, 1),
            'backward': (0, -1),
            'down': (1, 0),
            'up': (-1, 0),
            'diag_fd': (1, 1),    # Diagonal forward-down
            'diag_bd': (1, -1),   # Diagonal backward-down
            'diag_fu': (-1, 1),   # Diagonal forward-up
            'diag_bu': (-1, -1)   # Diagonal backward-up
        }

    # -----------------------------------------------------------------
    # --- 1. PUZZLE GENERATION METHODS
    # -----------------------------------------------------------------

    def generate_puzzle(self, word_file, rows, cols, output_puzzle, output_key):
        """
        This is the main public method for generating a new puzzle.
        It orchestrates the entire process from reading words
        to saving the final files.
        """
        print(f"starting puzzle generation ({rows}x{cols}) using '{word_file}'...")
        
        self.rows = rows
        self.columns = cols
        
        # Initialize empty grids
        # The 'key_grid' will only contain the placed words,
        # while the 'grid' will be filled with random letters.
        self.grid = [['_' for _ in range(self.columns)] for _ in range(self.rows)]
        self.key_grid = [['*' for _ in range(self.columns)] for _ in range(self.rows)]

        try:
            self._read_word_file(word_file)
        except FileNotFoundError:
            print(f"error: word file not found at '{word_file}'")
            return

        # Attempt to place all words from the list
        self._attempt_to_place_all_words()
        
        # Once words are placed, fill the remaining empty spots
        self._fill_empty_cells()
        
        # Save the completed puzzle and the key
        self._write_grid_to_file(self.grid, output_puzzle)
        self._write_grid_to_file(self.key_grid, output_key)
        
        print(f"successfully generated puzzle and key.")
        print(f"puzzle saved to: '{output_puzzle}'")
        print(f"key saved to: '{output_key}'")

    def _attempt_to_place_all_words(self):
        """
        This is the core of the generator. It loops through each word
        and tries to find a valid random location for it.
        """
        placed_words = []
        for word in self.word_list:
            word = word.strip().lower()
            if not word:
                continue

            # We'll try a limited number of times to place each word
            # to prevent an infinite loop if the grid is too full.
            max_attempts = 50 
            placed = False
            for _ in range(max_attempts):
                # Try to find a valid spot
                location = self._find_placement_location(word)
                if location:
                    r_start, c_start, direction_vector = location
                    self._place_word(word, r_start, c_start, direction_vector)
                    placed = True
                    placed_words.append(word)
                    break # Success, move to the next word
            
            if not placed:
                print(f"warning: could not find a place for word: '{word}'")
        
        # Update our word list to only include words we actually placed
        self.word_list = placed_words

    def _find_placement_location(self, word):
        """
        Tries to find a random valid starting coordinate (r, c)
        and direction (dr, dc) where the given word will fit.
        """
        # Create a shuffled list of directions to try
        shuffled_directions = list(self.directions.values())
        random.shuffle(shuffled_directions)
        
        for dr, dc in shuffled_directions:
            # Pick a random starting point
            r_start = random.randint(0, self.rows - 1)
            c_start = random.randint(0, self.columns - 1)
            
            # Check if the word fits at this location
            if self._check_fit(word, r_start, c_start, dr, dc):
                return (r_start, c_start, (dr, dc))
        
        # If we get through all directions and haven't found a fit
        return None

    def _check_fit(self, word, r_start, c_start, dr, dc):
        """
        Checks if a word can be placed at (r, c) in direction (dr, dc).
        A word can be placed if:
        1. It doesn't go out of the grid boundaries.
        2. It only overlaps with existing letters that are the same.
        """
        r, c = r_start, c_start
        for letter in word:
            # 1. Check for out-of-bounds
            if not (0 <= r < self.rows and 0 <= c < self.columns):
                return False
            
            # 2. Check for letter conflicts
            existing_letter = self.grid[r][c]
            if existing_letter != '_' and existing_letter != letter:
                return False
                
            # Move to the next letter's position
            r += dr
            c += dc
            
        return True

    def _place_word(self, word, r_start, c_start, direction_vector):
        """
        This single method replaces all 8 'write...' functions from
        the original script. By using the (dr, dc) vector, we can
        place any word in any direction with one simple loop.
        """
        dr, dc = direction_vector
        r, c = r_start, c_start
        for letter in word:
            self.grid[r][c] = letter
            self.key_grid[r][c] = letter
            # Move to the next position
            r += dr
            c += dc

    def _fill_empty_cells(self):
        """Fills all remaining '_' spaces with random letters."""
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for r in range(self.rows):
            for c in range(self.columns):
                if self.grid[r][c] == '_':
                    self.grid[r][c] = random.choice(alphabet)

    # -----------------------------------------------------------------
    # --- 2. PUZZLE SOLVING METHODS
    # -----------------------------------------------------------------

    def solve_puzzle(self, puzzle_file, word_file, output_json):
        """
        Main public method for solving an existing puzzle.
        It orchestrates reading the files, finding the words,
        and writing the JSON solution.
        """
        print(f"starting puzzle solver for '{puzzle_file}'...")
        try:
            self._read_grid_file(puzzle_file)
            self._read_word_file(word_file)
        except FileNotFoundError as e:
            print(f"error: could not read file. {e}")
            return
            
        # This is where the core solving logic happens
        solution = self._find_all_words()
        
        # Save the solution to the specified JSON file
        self.export_solution_to_json(solution, output_json)
        print(f"solving complete. results saved to '{output_json}'")

    def _find_all_words(self):
        """
        This is the main solver logic. It iterates through every cell
        in the grid. From each cell, it "looks" in all 8 directions
        to see if any word from our list starts there.
        """
        # Store our word list in a 'set' for O(1) lookups
        word_set = set(self.word_list)
        found_words = {}

        # **FIX:** handle the case of an empty word list to prevent errors
        if not word_set:
            print("word list is empty. nothing to solve.")
            return {}
        
        # **FIX:** get the max word length *once* for efficiency
        max_len = max(len(w) for w in word_set)

        for r in range(self.rows):
            for c in range(self.columns):
                # From this cell (r, c), check all 8 directions
                for direction_name, (dr, dc) in self.directions.items():
                    
                    # Check for words starting at (r, c) in this direction
                    found_word, end_coords = self._check_direction(word_set, max_len, r, c, dr, dc)
                    
                    if found_word:
                        # We found one! Store it in our solution dict.
                        # We only store the *first* finding.
                        if found_word not in found_words:
                            found_words[found_word] = {
                                "direction": direction_name,
                                "start": (r, c),
                                "end": end_coords
                            }

        # Check for any words we *didn't* find
        for word in self.word_list:
            if word not in found_words:
                found_words[word] = "word not found"
                
        return found_words

    def _check_direction(self, word_set, max_len, r_start, c_start, dr, dc):
        """
        Starting from (r, c), builds a string in the direction (dr, dc)
        and checks if it's in our word list.
        'max_len' is pre-calculated for efficiency.
        """
        current_string = ""
        r, c = r_start, c_start
        
        for _ in range(max_len):
            # 1. Check for out-of-bounds
            if not (0 <= r < self.rows and 0 <= c < self.columns):
                break # Reached the edge
            
            # 2. Add the letter and check for a match
            current_string += self.grid[r][c]
            if current_string in word_set:
                # We found a word!
                return current_string, (r, c)
                
            # 3. Move to the next letter
            r += dr
            c += dc
            
        # We checked all the way and found no word
        return None, None

    # -----------------------------------------------------------------
    # --- 3. UTILITY METHODS (File I/O)
    # -----------------------------------------------------------------

    def _read_word_file(self, filename):
        """
        Reads a .txt word bank file and populates self.word_list.
        Using pathlib.Path is a modern way to handle file paths.
        """
        filepath = Path(filename)
        if not filepath.exists():
            raise FileNotFoundError(f"word file '{filename}' not found.")
            
        with open(filepath, 'r') as f:
            # We use .strip() to remove newline characters
            # and .lower() to make everything consistent.
            self.word_list = [line.strip().lower() for line in f if line.strip()]

    def _read_grid_file(self, filename):
        """
        Reads a .txt puzzle file and populates self.grid.
        It also sets self.rows and self.columns based on the file.
        """
        filepath = Path(filename)
        if not filepath.exists():
            raise FileNotFoundError(f"puzzle file '{filename}' not found.")
            
        with open(filepath, 'r') as f:
            grid = []
            for line in f:
                # We split the line by spaces and filter out any empty strings
                letters = [letter for letter in line.strip().split(' ') if letter]
                if letters:
                    grid.append(letters)
        
        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0]) if self.rows > 0 else 0

    def _write_grid_to_file(self, grid, filename):
        """
        Writes a given grid (puzzle or key) to a .txt file
        with spaces between letters.
        """
        filepath = Path(filename)
        with open(filepath, 'w') as f:
            for row in grid:
                f.write(' '.join(row) + '\n')
                
    def export_solution_to_json(self, solution, filename):
        """
        Writes the final solution dictionary to a .json file.
        'indent=4' makes the file human-readable.
        """
        filepath = Path(filename)
        with open(filepath, 'w') as json_file:
            json.dump(solution, json_file, indent=4)


# ---------------------------------------------------------------------------
# COMMAND-LINE INTERFACE
# ---------------------------------------------------------------------------

def main():
    """
    This is the main entry point for the script.
    
    Instead of a series of input() prompts, we use 'argparse'
    to create a proper command-line tool. This is much more
    flexible and is standard practice for Python scripts.
    
    We define two 'subcommands': 'generate' and 'solve'.
    """
    
    # 1. Create the main parser
    parser = argparse.ArgumentParser(
        description="A tool to generate or solve word search puzzles.",
        epilog="example: %(prog)s generate -w words.txt -r 15 -c 15"
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="the action to perform")

    # 2. Create the 'generate' command parser
    gen_parser = subparsers.add_parser(
        "generate", 
        help="generate a new word search puzzle"
    )
    gen_parser.add_argument(
        "-w", "--words", 
        required=True, 
        help="path to the .txt file containing the word list"
    )
    gen_parser.add_argument(
        "-r", "--rows", 
        required=True, 
        type=int, 
        help="number of rows for the puzzle"
    )
    gen_parser.add_argument(
        "-c", "--cols", 
        required=True, 
        type=int, 
        help="number of columns for the puzzle"
    )
    gen_parser.add_argument(
        "--op", "--output-puzzle", 
        dest="output_puzzle", 
        default="wordPuzzle_new.txt", 
        help="filename for the generated puzzle (default: wordPuzzle_new.txt)"
    )
    gen_parser.add_argument(
        "--ok", "--output-key", 
        dest="output_key", 
        default="wordPuzzle_key.txt", 
        help="filename for the puzzle key (default: wordPuzzle_key.txt)"
    )

    # 3. Create the 'solve' command parser
    solve_parser = subparsers.add_parser(
        "solve", 
        help="solve an existing word search puzzle"
    )
    solve_parser.add_argument(
        "-p", "--puzzle", 
        required=True, 
        help="path to the .txt puzzle file to solve"
    )
    solve_parser.add_argument(
        "-w", "--words", 
        required=True, 
        help="path to the .txt file containing the word list to find"
    )
    solve_parser.add_argument(
        "-o", "--output", 
        dest="output_json", 
        default="wordSearchResults.json", 
        help="filename for the JSON solution output (default: wordSearchResults.json)"
    )

    # 4. Parse the arguments provided by the user
    args = parser.parse_args()

    # 5. Create our WordSearch object and run the correct command
    # This is the beauty of OOP: we create one object
    # and just call the method we need.
    game = WordSearch()

    if args.command == "generate":
        if args.rows <= 0 or args.cols <= 0:
            print("error: rows and columns must be positive numbers.")
            sys.exit(1)
        game.generate_puzzle(
            word_file=args.words, 
            rows=args.rows, 
            cols=args.cols,
            output_puzzle=args.output_puzzle,
            output_key=args.output_key
        )
        
    elif args.command == "solve":
        game.solve_puzzle(
            puzzle_file=args.puzzle, 
            word_file=args.words,
            output_json=args.output_json
        )

if __name__ == "__main__":
    # This standard line means 'run the main() function
    # only if this script is executed directly'.
    main()