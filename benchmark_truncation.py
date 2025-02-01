import os
import sqlite3
import subprocess
import re
import time
import random

# Configuration
DATABASE_PATH = "result1_prefix.db"  # Source database
REPAIR_OUTPUT_DIR = "repair_results"
REPAIR_ALGORITHMS = ["DDMax", "bRepair", "DDMaxG", "Antlr"]

PROJECT_PATHS = {
    "ini": "project/fsynth-subjects/ini/ini",
    "json": "project/fsynth-subjects/cjson/cjson",
    "lisp": "project/fsynth-subjects/sexp-parser/sexp",
    "c": "project/fsynth-subjects/tiny/tiny"
}

valid_formats = ["ini","json,","lisp","c"]

def get_user_selected_formats():
    """Allow the user to select which formats to process."""
    return valid_formats


def validate_with_external_tool(file_path: str, format_key: str) -> bool:
    """Validate a file using the corresponding parser."""
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
            timeout=30  # Parser time limit
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Validation timeout for format '{format_key}'")
        return False
    except Exception as e:
        print(f"[ERROR] Could not run validation tool for format '{format_key}': {e}")
        return False


def levenshtein_distance(a: str, b: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.
    """
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
                dp[i - 1][j] + 1,    # Deletion
                dp[i][j - 1] + 1,    # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )

    return dp[-1][-1]


def extract_oracle_info(stdout: str):
    """Extracts iterations, correct, incorrect, and incomplete oracle runs from output."""
    match = re.search(r"\*\*\* Number of required oracle runs: (\d+) correct: (\d+) incorrect: (\d+) incomplete: (\d+) \*\*\*", stdout)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))  # iterations, correct, incorrect, incomplete
    return 0, 0, 0, 0  # Default values


def repair_and_update_entry(cursor, conn, entry):
    """
    Rerun the repair for a given database entry and update the database with the new results.
    """
    id_, format, algorithm, original_text, broken_text = entry
    print(f"[INFO] Processing entry ID {id_} (Format: {format}, Algorithm: {algorithm})")

    # Write the broken text to a temporary file
    input_file = f"temp_{random.randint(0, 10000)}_input.{format}"
    output_file = f"{REPAIR_OUTPUT_DIR}/repair_{id_}_output.txt"

    with open(input_file, "w") as f:
        f.write(broken_text)

    iterations, correct_runs, incorrect_runs, incomplete_runs = 0, 0, 0, 0
    repaired_text = ""
    fixed = False
    repair_time = 0

    # Compute distances
    distance_original_broken = levenshtein_distance(original_text, broken_text)
    distance_broken_repaired = -1
    distance_original_repaired = -1

    try:
        if algorithm == "bRepair":
            cmd = ["./brepair", PROJECT_PATHS.get(format, ""), input_file, output_file]
        else:
            cmd = ["java", "-jar", "./project/bin/fsynth.jar", "-r", "-a", algorithm, "-i", input_file, "-o", output_file]

        # Run the repair process
        start_time = time.time()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=240)
        repair_time = time.time() - start_time

        # Extract oracle run details
        iterations, correct_runs, incorrect_runs, incomplete_runs = extract_oracle_info(stdout)

        # Log outputs for debugging
        print(f"STDOUT for ID {id_}:\n{stdout}")
        print(f"STDERR for ID {id_}:\n{stderr}")

        if process.returncode == 0 and os.path.exists(output_file):
            with open(output_file, "r") as f:
                repaired_text = f.read()
            fixed = validate_with_external_tool(output_file, format)

            # Compute distances if repaired text is available
            distance_broken_repaired = levenshtein_distance(broken_text, repaired_text)
            distance_original_repaired = levenshtein_distance(original_text, repaired_text)

    except subprocess.TimeoutExpired:
        print(f"[ERROR] Repair timeout for entry ID {id_}")
    except Exception as e:
        print(f"[ERROR] Repair failed for entry ID {id_}: {e}")

    # Update the database
    cursor.execute("""
        UPDATE results
        SET repaired_text = ?, fixed = ?, iterations = ?, repair_time = ?,
            correct_runs = ?, incorrect_runs = ?, incomplete_runs = ?,
            distance_original_broken = ?, distance_broken_repaired = ?, distance_original_repaired = ?
        WHERE id = ?
    """, (repaired_text, fixed, iterations, repair_time,
          correct_runs, incorrect_runs, incomplete_runs,
          distance_original_broken, distance_broken_repaired, distance_original_repaired, id_))

    conn.commit()  # Save changes

    # Clean up temporary files
    os.remove(input_file) if os.path.exists(input_file) else None
    os.remove(output_file) if os.path.exists(output_file) else None


def rerun_repairs():
    """
    Rerun repairs for only the selected formats in the database.
    """
    selected_formats = get_user_selected_formats()
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Add new columns if they do not exist
    cursor.execute("PRAGMA table_info(results)")
    existing_columns = {col[1] for col in cursor.fetchall()}
    
    for column in ["correct_runs", "incorrect_runs", "incomplete_runs"]:
        if column not in existing_columns:
            cursor.execute(f"ALTER TABLE results ADD COLUMN {column} INTEGER DEFAULT 0")

    cursor.execute("""
        SELECT id, format, algorithm, original_text, broken_text
        FROM results
    """)
    entries = cursor.fetchall()

    filtered_entries = [entry for entry in entries if entry[1] in selected_formats]

    for entry in filtered_entries:
        repair_and_update_entry(cursor, conn, entry)

    conn.close()
    print("[INFO] All selected repairs have been completed!")


if __name__ == "__main__":
    rerun_repairs()