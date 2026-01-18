import csv
import re
import os
import sys
import subprocess

def read_file_content(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.docx':
        try:
            import docx
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except ImportError:
            print("Error: python-docx library not found. Please install it (pip install python-docx) to read .docx files.")
            return None
        except Exception as e:
            print(f"Error reading .docx file: {e}")
            return None

    elif ext == '.doc':
        try:
            # Use textutil on macOS to convert .doc to stdout as txt
            process = subprocess.run(
                ['textutil', '-convert', 'txt', '-stdout', file_path],
                capture_output=True,
                text=True,
                check=True
            )
            return process.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error reading .doc file with textutil: {e}")
            return None
        except FileNotFoundError:
            print("Error: textutil command not found. Reading .doc files requires macOS or an installed textutil equivalent.")
            return None
        except Exception as e:
            print(f"Error reading .doc file: {e}")
            return None
    
    else:
        # Default to assuming it's a text file
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try a fallback encoding if utf-8 fails
            try:
                with open(file_path, mode='r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                 print(f"Error reading input file: {e}")
                 return None
        except Exception as e:
            print(f"Error reading input file: {e}")
            return None

def calculate_affinity():
    # 1. Get input file name
    if len(sys.argv) > 1:
        input_file_path = sys.argv[1]
    else:
        input_file_path = input("Enter the file name: ").strip()

    # Expand user path if necessary (e.g. ~/.gemini/...)
    input_file_path = os.path.expanduser(input_file_path)

    if not os.path.exists(input_file_path):
        print(f"Error: File '{input_file_path}' not found.")
        return

    # 2. Check for affinity_scores.csv
    # Assuming affinity_scores.csv is in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scores_file_path = os.path.join(script_dir, "affinity_scores.csv")
    
    if not os.path.exists(scores_file_path):
        # Fallback: check current working directory
        scores_file_path = "affinity_scores.csv"
        if not os.path.exists(scores_file_path):
            print("Error: 'affinity_scores.csv' not found in script directory or current directory.")
            return

    # 3. Load affinity scores
    scores_dict = {}
    # We keep a list to iterate over for matching
    affinity_data = []

    try:
        with open(scores_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None) # Skip header if present
            # Heuristic: check if first row looks like header
            if header and header[0].lower() == 'word' and header[1].lower() == 'score':
                pass # It was the header
            else:
                # If specifically no header text, reset file pointer or process header as row
                # The provided file has "Word,Score" as header based on previous `view_file`.
                pass

            for row in reader:
                if len(row) >= 2:
                    word = row[0].strip()
                    try:
                        score = int(row[1].strip())
                        affinity_data.append((word, score))
                    except ValueError:
                        continue # Skip invalid scores
    except Exception as e:
        print(f"Error reading affinity scores: {e}")
        return

    # 4. Read input text
    text_content = read_file_content(input_file_path)
    if text_content is None:
        return

    # 5. Calculate scores
    results = []
    
    # We want valid word boundaries, but also need to handle cases like "can't"
    # The simplest regex that respects phrases is to iterate and search.
    # Note: re.escape escapes special regex chars.
    
    for word, score in affinity_data:
        # Construct pattern
        # \b matches word boundary.
        # For phrases like "bad luck", \bbad luck\b works.
        # For "can't", \bcan't\b works if ' is treated as word char? 
        # Actually in Python re, ' is NOT a word char. So \bcan't\b matches "can" (boundary) 't (boundary). 
        # This is tricky. "can't" -> \bcan't\b matches "can" then "'t". 
        # \b is between \w and \W.
        # " can't " -> space(W) c(w) ... n(w) '(W) t(w) space(W).
        # \b matches before c. \b matches between n and '. \b matches between ' and t. \b matches after t.
        # So `\bcan't\b` will fail because `re.escape("can't")` is `can\'t`.
        # Pattern: `\bcan\'t\b`
        # Text: ` can't `
        # \b match before c? Yes.
        # Match `can\'t`? 
        #   c matches. a matches. n matches. ' matches. t matches.
        # \b match after t? Yes.
        # BUT: internal `\b`?
        # \b is zero-width assertion.
        # It doesn't consume characters.
        # So `\b`+`can't`+`\b` should match ` can't ` assuming no internal boundary issues in the regex string itself.
        # Wait, does `\b` apply to the string "can't"?
        # No, `\b` is an assertion.
        # `re.compile(r"\bcan't\b")` matches "can't".
        # Let's verify this handling.
        # However, to be extra safe with punctuation-heavy terms in CSV, we can use a slightly looser check or rely on `\b` being good enough for standard English.
        
        # Prevent partial matches with apostrophes (e.g. "won" matching "won't")
        pattern = r"(?<!['’])\b" + re.escape(word) + r"\b(?!['’])"
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        count = len(matches)
        
        if count > 0:
            final_score = score * count
            results.append([word, count, score, final_score])

    # 6. Write output
    input_dir = os.path.dirname(os.path.abspath(input_file_path))
    base_name = os.path.splitext(os.path.basename(input_file_path))[0]
    output_filename = f"{base_name}_affinity_results.csv"
    output_path = os.path.join(input_dir, output_filename)

    try:
        with open(output_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Word", "Count", "Affinity Score", "Final Score"])
            writer.writerows(results)
        print(f"Success! Results saved to '{output_path}'")
        
        # Calculate total score just for display? The user didn't ask for a total sum, just the table.
        
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    calculate_affinity()
