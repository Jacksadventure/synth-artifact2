#!/usr/bin/env python3
import os
import sqlite3
import subprocess
import re
import time
import random

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
DATABASE_PATH = "result1.db"  # Name of the new database to create
REPAIR_OUTPUT_DIR = "repair_results"  # Directory where repair outputs are stored
os.makedirs(REPAIR_OUTPUT_DIR, exist_ok=True)

# Possible repair algorithms you want to test
REPAIR_ALGORITHMS = ["DDMax", "bRepair", "DDMaxG", "Antlr"]

# Paths to the external format validators (adjust as needed)
PROJECT_PATHS = {
    "ini":  "project/fsynth-subjects/ini/ini",
    "json": "project/fsynth-subjects/cjson/cjson",
    "lisp": "project/fsynth-subjects/sexp-parser/sexp",
    "c":    "project/fsynth-subjects/tiny/tiny"
}

# Valid formats/folders to process
VALID_FORMATS = ["ini", "json", "lisp", "c"]

# Parser timeout (in seconds)
VALIDATION_TIMEOUT = 30

# Repair timeout (in seconds)
REPAIR_TIMEOUT = 240

# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------

def create_database(db_path: str):
    """
    Creates a new SQLite database (or overwrites if it already exists).
    This function will create a 'results' table with columns that store
    original/corrupted text, repaired text, and various repair metrics.
    """
    if os.path.exists(db_path):
        print(f"[WARNING] Database '{db_path}' already exists. It will be reused/overwritten.")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            format TEXT,
            file_id INTEGER,
            corrupted_index INTEGER,
            algorithm TEXT,
            original_text TEXT,
            broken_text TEXT,
            repaired_text TEXT,
            fixed INTEGER,
            iterations INTEGER,
            repair_time REAL,
            correct_runs INTEGER,
            incorrect_runs INTEGER,
            incomplete_runs INTEGER,
            distance_original_broken INTEGER,
            distance_broken_repaired INTEGER,
            distance_original_repaired INTEGER
        )
    """)
    conn.commit()
    conn.close()
    print(f"[INFO] Created/checked table 'results' in database '{db_path}'.")


def load_test_samples_from_folders(base_dir: str, format_key: str):
    """
    Scans `base_dir/format_key` subfolders named 'original' and 'corrupted',
    collects (original_text, corrupted_text) pairs based on file naming:
        original_<N>.<ext>  
        corrupted_<N>_<X>.<ext>
    Returns a list of tuples: (file_id, corrupted_index, original_text, corrupted_text).

    Example structure:
        generated_files/
          └── c
              ├── original
              │   ├── original_7.c
              │   ├── original_8.c
              └── corrupted
                  ├── corrupted_7_1.c
                  ├── corrupted_7_2.c
                  ├── corrupted_8_1.c
                  ...
    """
    format_dir = os.path.join(base_dir, format_key)
    original_dir = os.path.join(format_dir, "original")
    corrupted_dir = os.path.join(format_dir, "corrupted")

    if not os.path.isdir(original_dir) or not os.path.isdir(corrupted_dir):
        print(f"[WARNING] Missing 'original' or 'corrupted' folder for format '{format_key}'")
        return []

    # Read all original files
    originals = {}
    for fname in os.listdir(original_dir):
        if fname.endswith(f".{format_key}") and fname.startswith("original_"):
            match = re.match(r"original_(\d+)\." + format_key, fname)
            if match:
                file_id = int(match.group(1))
                with open(os.path.join(original_dir, fname), 'r', encoding='utf-8') as f:
                    originals[file_id] = f.read()

    # Read all corrupted files
    corrupteds = {}
    for fname in os.listdir(corrupted_dir):
        if fname.endswith(f".{format_key}") and fname.startswith("corrupted_"):
            match = re.match(r"corrupted_(\d+)_(\d+)\." + format_key, fname)
            if match:
                original_id = int(match.group(1))
                corrupted_index = int(match.group(2))
                with open(os.path.join(corrupted_dir, fname), 'r', encoding='utf-8') as f:
                    text = f.read()
                if original_id not in corrupteds:
                    corrupteds[original_id] = {}
                corrupteds[original_id][corrupted_index] = text

    # Combine original with each corrupted variant
    test_samples = []
    for file_id, orig_text in originals.items():
        if file_id in corrupteds:
            for cindex, ctext in corrupteds[file_id].items():
                test_samples.append((file_id, cindex, orig_text, ctext))
        else:
            # If there are no corrupted files for this original, skip or handle accordingly
            pass

    return test_samples


def insert_test_samples_to_db(db_path: str, format_key: str, test_samples: list):
    """
    Insert the given list of (file_id, corrupted_index, original_text, corrupted_text)
    into the 'results' table in the database, for the specified format.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert each entry with a placeholder algorithm; we'll run multiple or update later
    for (file_id, cindex, orig_text, broken_text) in test_samples:
        for alg in REPAIR_ALGORITHMS:
            cursor.execute("""
                INSERT INTO results (format, file_id, corrupted_index, algorithm,
                                     original_text, broken_text,
                                     repaired_text, fixed, iterations, repair_time,
                                     correct_runs, incorrect_runs, incomplete_runs,
                                     distance_original_broken, distance_broken_repaired, distance_original_repaired)
                VALUES (?, ?, ?, ?, ?, ?, '', 0, 0, 0.0, 0, 0, 0, 0, 0, 0)
            """, (format_key, file_id, cindex, alg, orig_text, broken_text))
    conn.commit()
    conn.close()


def validate_with_external_tool(file_path: str, format_key: str) -> bool:
    """
    Validate a repaired file by running the corresponding parser or tool.
    Return True if return code == 0, else False.
    """
    executable_path = PROJECT_PATHS.get(format_key)
    if not executable_path or not os.path.exists(executable_path):
        print(f"[WARNING] No executable found for format '{format_key}'")
        return False

    try:
        result = subprocess.run(
            [executable_path, file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=VALIDATION_TIMEOUT
        )
        return (result.returncode == 0)
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Validation timeout for '{file_path}', format '{format_key}'")
        return False
    except Exception as e:
        print(f"[ERROR] Could not run validation tool for format '{format_key}': {e}")
        return False


def levenshtein_distance(a: str, b: str) -> int:
    """Calculate the Levenshtein distance between two strings."""
    if not a: return len(b)
    if not b: return len(a)

    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        dp[i][0] = i
    for j in range(len(b) + 1):
        dp[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,       # Deletion
                dp[i][j - 1] + 1,       # Insertion
                dp[i - 1][j - 1] + cost # Substitution
            )
    return dp[-1][-1]


def extract_oracle_info(stdout: str):
    """
    Example parser for lines like:
        *** Number of required oracle runs: 10 correct: 5 incorrect: 3 incomplete: 2 ***
    Adjust if your actual output is different.
    """
    match = re.search(r"\*\*\* Number of required oracle runs: (\d+) correct: (\d+) incorrect: (\d+) incomplete: (\d+) \*\*\*", stdout)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))
    return 0, 0, 0, 0


def repair_and_update_entry(cursor, conn, row):
    """
    Given a single row from the 'results' table, run the repair tool, measure results,
    and update the row in the database.
    """
    (id_, format_key, file_id, corrupted_index, algorithm,
     original_text, broken_text, _repaired, _fixed, _iter, _rtime,
     _correct, _incorrect, _incomplete, _distOB, _distBR, _distOR) = row

    print(f"[INFO] Repairing ID={id_}, format={format_key}, algorithm={algorithm}, file_id={file_id}, corrupted_index={corrupted_index}")

    # Prepare temporary input and output files
    ext = format_key
    input_file = f"temp_{id_}_{random.randint(0, 9999)}_input.{ext}"
    output_file = os.path.join(REPAIR_OUTPUT_DIR, f"repair_{id_}_output.{ext}")

    with open(input_file, "w", encoding="utf-8") as f:
        f.write(broken_text)

    distance_original_broken = levenshtein_distance(original_text, broken_text)
    distance_broken_repaired = -1
    distance_original_repaired = -1

    # By default, we mark as not fixed
    repaired_text = ""
    fixed = 0
    iterations, correct_runs, incorrect_runs, incomplete_runs = 0, 0, 0, 0
    repair_time = 0.0

    # Choose the repair command
    if algorithm == "bRepair":
        # Example usage of a hypothetical bRepair binary
        cmd = ["./brepair", PROJECT_PATHS.get(format_key, ""), input_file, output_file]
    else:
        # Example usage of your fsynth.jar approach
        cmd = [
            "java", "-jar", "./project/bin/fsynth.jar",
            "-r", "-a", algorithm,
            "-i", input_file,
            "-o", output_file
        ]

    try:
        start_time = time.time()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate(timeout=REPAIR_TIMEOUT)
        repair_time = time.time() - start_time

        # Extract oracle info (optional)
        iterations, correct_runs, incorrect_runs, incomplete_runs = extract_oracle_info(stdout)

        print(f"--- STDOUT (ID={id_}) ---\n{stdout}\n")
        print(f"--- STDERR (ID={id_}) ---\n{stderr}\n")

        if proc.returncode == 0 and os.path.exists(output_file):
            # Read the repaired output
            with open(output_file, "r", encoding="utf-8") as rf:
                repaired_text = rf.read()

            # Validate the repaired file
            if validate_with_external_tool(output_file, format_key):
                fixed = 1

            # Compute Levenshtein distances
            distance_broken_repaired = levenshtein_distance(broken_text, repaired_text)
            distance_original_repaired = levenshtein_distance(original_text, repaired_text)

    except subprocess.TimeoutExpired:
        print(f"[ERROR] Repair timed out for entry ID={id_}")
    except Exception as e:
        print(f"[ERROR] Repair failed for entry ID={id_}: {e}")
    finally:
        # Clean up temp files
        if os.path.exists(input_file):
            os.remove(input_file)
        if os.path.exists(output_file):
            os.remove(output_file)

    # Update the database record
    cursor.execute("""
        UPDATE results
        SET repaired_text = ?, fixed = ?, iterations = ?, repair_time = ?,
            correct_runs = ?, incorrect_runs = ?, incomplete_runs = ?,
            distance_original_broken = ?, distance_broken_repaired = ?, distance_original_repaired = ?
        WHERE id = ?
    """, (
        repaired_text, fixed, iterations, repair_time,
        correct_runs, incorrect_runs, incomplete_runs,
        distance_original_broken, distance_broken_repaired, distance_original_repaired,
        id_
    ))
    conn.commit()


def rerun_repairs_for_selected_formats(db_path: str, selected_formats=None):
    """
    Re-run (or run for the first time) repairs for the specified formats.
    If selected_formats is None, it will use all in VALID_FORMATS.
    """
    if not selected_formats:
        selected_formats = VALID_FORMATS

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch entries for the desired formats
    cursor.execute("""
        SELECT id, format, file_id, corrupted_index, algorithm,
               original_text, broken_text, repaired_text, fixed,
               iterations, repair_time, correct_runs, incorrect_runs,
               incomplete_runs, distance_original_broken, distance_broken_repaired,
               distance_original_repaired
        FROM results
    """)
    entries = cursor.fetchall()

    # Filter only those in the selected formats
    filtered_entries = [row for row in entries if row[1] in selected_formats]

    print(f"[INFO] Found {len(filtered_entries)} entries to (re)process.")
    for row in filtered_entries:
        repair_and_update_entry(cursor, conn, row)

    conn.close()
    print("[INFO] Repair process completed!")


# ------------------------------------------------------------------------------
# Main script flow
# ------------------------------------------------------------------------------
def main():
    # 1) Create or reuse the database
    create_database(DATABASE_PATH)

    # 2) For each format in VALID_FORMATS, load test samples from folders
    base_dir = "generated_files"
    for fmt in VALID_FORMATS:
        samples = load_test_samples_from_folders(base_dir, fmt)
        if samples:
            # 3) Insert each sample into the 'results' table for *each* algorithm
            insert_test_samples_to_db(DATABASE_PATH, fmt, samples)
        else:
            print(f"[INFO] No samples found for format '{fmt}' in '{base_dir}'")

    # 4) Now run or re-run the repairs for the newly inserted entries
    rerun_repairs_for_selected_formats(DATABASE_PATH, selected_formats=VALID_FORMATS)


if __name__ == "__main__":
    main()