# Wordle Solver README

## Project Overview:
This project is part of an NLP class project and implements a Wordle solver using Python. Wordle is a popular word puzzle game where players attempt to guess a secret five-letter word. After each guess, the game provides feedback indicating which letters are correct, misplaced, or not present in the word.

## Solver Description:
The solver utilizes various strategies to guess the target word efficiently:
1. **Entropy-Based Word Selection:** Words from a wordlist are evaluated based on their entropy, prioritizing words with lower entropy (i.e., higher predictability).
2. **Letter Frequency Analysis:** The solver analyzes the frequency of letters in possible words and adjusts its guesses accordingly.
3. **Pattern Recognition:** It identifies patterns in the feedback received from previous guesses to refine future guesses.

## How to Run the Game:
1. **Install Dependencies:** Ensure you have Python installed on your system along with the required packages listed in the `requirements.txt` file.
2. **Download Wordlist:** Download the `wordlist.yaml` file containing a list of valid words for the game.
3. **Run the Game:**
   - **Automatic Mode:** Run the game in automatic mode using the command `python main.py --r [number_of_runs]`, where `[number_of_runs]` specifies the number of automated runs to execute. This mode evaluates the solver's performance statistically.
   - **Manual Mode:** Play the game manually by running `python main.py` without any arguments. Follow the instructions displayed in the console to input your guesses manually.

## Project Author: Pietro Del Bianco

## Acknowledgments:
- This project was completed as part of an NLP class project.
- The `wordle.py` module is used to interact with the Wordle game environment.
- The project also utilizes the `rich` library for enhanced console output.

## Disclaimer:
This Wordle solver is designed for educational purposes and to demonstrate various techniques in natural language processing and game-solving algorithms. It is not intended for use in competitive or commercial environments.
