#!/usr/bin/env python3
"""
trim_results.py  –  keep only the newest 300 rows in table `results`

Usage
-----
python trim_results.py result1.db
"""

import sqlite3, sys, os

MAX_ROWS = 300          # target size

def trim(db_path: str):
    if not os.path.exists(db_path):
        sys.exit(f"[ERR] DB file '{db_path}' not found")

    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM results")
    total = cur.fetchone()[0]
    print(f"[INFO] rows in `results`: {total}")

    if total <= MAX_ROWS:
        print("[INFO] nothing to trim")
        conn.close()
        return

    # delete oldest rows by ascending id, keep the most recent MAX_ROWS
    rows_to_delete = total - MAX_ROWS
    cur.execute(
        "DELETE FROM results "
        "WHERE id IN (SELECT id FROM results ORDER BY id ASC LIMIT ?)",
        (rows_to_delete,))
    conn.commit()
    conn.close()
    print(f"[DONE] deleted {rows_to_delete} oldest row(s), kept {MAX_ROWS}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python trim_results.py <sqlite_db>")
    trim(sys.argv[1])