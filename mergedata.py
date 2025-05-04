#!/usr/bin/env python3
"""
merge_sqlite_results.py
-----------------------
Merge multiple SQLite files that each contain a table named `results`
into one destination SQLite DB.

Usage
-----
python merge_sqlite_results.py dest.db source1.db source2.db ...

Notes
-----
* Assumes all `results` tables share exactly the same schema.
* Copies rows in ID order; `id` column will re‑auto‑increment in dest.
* If a column list changes, adjust `COLUMNS` accordingly.
"""

import sqlite3
import sys
import os

# List of columns you want to copy (omit dest `id` to let it auto‑increment)
COLUMNS = [
    "format", "file_id", "corrupted_index", "algorithm",
    "original_text", "broken_text", "repaired_text", "fixed",
    "iterations", "repair_time", "correct_runs", "incorrect_runs",
    "incomplete_runs", "distance_original_broken", "distance_broken_repaired",
    "distance_original_repaired"
]

def ensure_table(conn: sqlite3.Connection):
    """Create the `results` schema if not exists (same as previous scripts)."""
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS results(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {', '.join(f'{col} TEXT' for col in COLUMNS)}  -- store all as TEXT for simplicity
        );
    """)
    conn.commit()

def merge_into(dest_db: str, src_paths: list[str]):
    if not src_paths:
        sys.exit("[ERR] No source DBs provided")

    dest = sqlite3.connect(dest_db)
    ensure_table(dest)
    dest_cur = dest.cursor()

    col_list = ", ".join(COLUMNS)
    placeholders = ", ".join("?" * len(COLUMNS))
    insert_sql = f"INSERT INTO results ({col_list}) VALUES ({placeholders})"

    total_inserted = 0
    for src_path in src_paths:
        if not os.path.exists(src_path):
            print(f"[WARN] Skip missing file: {src_path}")
            continue
        src = sqlite3.connect(src_path)
        src.row_factory = sqlite3.Row
        src_cur = src.cursor()
        try:
            src_cur.execute(f"SELECT {col_list} FROM results ORDER BY id ASC")
        except sqlite3.OperationalError as e:
            print(f"[WARN] {src_path} has no 'results' table? -> {e}")
            src.close(); continue

        rows = src_cur.fetchall()
        dest_cur.executemany(insert_sql, [tuple(r[col] for col in COLUMNS) for r in rows])
        dest.commit()
        inserted = len(rows)
        total_inserted += inserted
        print(f"[INFO] {src_path}: copied {inserted} rows")
        src.close()

    dest.close()
    print(f"[DONE] total inserted into {dest_db}: {total_inserted}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: python merge_sqlite_results.py dest.db src1.db src2.db ...")
    dest, *sources = sys.argv[1:]
    merge_into(dest, sources)