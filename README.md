# AffinityScore

A Python tool to calculate affinity scores from text documents based on a predefined list of words and their weights.

## Functionality
- **Affinity Calculation**: Reads a document, counts occurrences of specific words (defined in `affinity_scores.csv`), and calculates a total affinity score.
- **File Support**:
  - `.txt` (Plain text)
  - `.docx` (Microsoft Word)
  - `.doc` (Legacy Microsoft Word - **macOS only**)

## Prerequisites
- Python 3.x installed on your system.

## Installation

1.  Open a terminal or command prompt.
2.  Navigate to the project directory.
3.  Run the installation script to set up dependencies.

    **For macOS/Linux:**
    ```bash
    ./setup.sh
    ```
    (You might need to make it executable first with `chmod +x setup.sh`)

    **For Windows:**
    Double-click `setup.bat` or run:
    ```cmd
    setup.bat
    ```

    These scripts will:
    - Check if Python is installed.
    - Install required Python packages (e.g., `python-docx`) from `requirements.txt`.
    - Check for OS-specific tools (like `textutil` on macOS for `.doc` support).

## Usage

1.  Ensure `affinity_scores.csv` is in the same directory (or update the script to point to it).
2.  Run the calculator:

    ```bash
    python affinity_calculator.py
    ```

3.  When prompted, enter the file name (including extension) you want to analyze (e.g., `Shirley_Jackson.docx` or `test.txt`).
4.  The script will generate a new CSV file (e.g., `Shirley_Jackson_affinity_results.csv`) containing the detailed score breakdown.
