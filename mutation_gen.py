#!/usr/bin/env python3
"""
mutate_and_store.py
-------------------
Traverse a directory, try to mutate each file until 10 distinct mutation
positions render the file un-parsable by an external validator.  Store every
(original_text, mutated_text) pair together with metadata in a SQLite DB.

Usage
-----
python mutate_and_store.py \
       --folder  ./data \
       --validator /usr/local/bin/ini-linter \
       --database mutations.sqlite

Arguments
---------
--folder     Path to the folder containing files to process (recursive).
--validator  Executable used to validate a file; exit-code 0 = OK.
--database   SQLite file to create / append to.
--max-attempts  Maximum mutation attempts per file (default 10_000).
--seed       RNG seed for reproducibility (optional).

Mutation strategy
-----------------
Randomly pick a byte offset, replace that byte with a different printable ASCII
character.  Each successful mutation position must be unique for that file.
"""

import argparse
import os
import random
import sqlite3
import string
import subprocess
import sys
from pathlib import Path
from typing import List, Set


PRINTABLE_ASCII = [c.encode() for c in string.printable if c not in ("\n", "\r")]


# --------------------------------------------------------------------------- #
def run_validator(exe: str, path: Path) -> bool:
    """Return True if validator EXIT STATUS == 0."""
    try:
        res = subprocess.run(
            [exe, str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
        return res.returncode == 0
    except Exception:
        return False  # treat crash/timeout as failure (cannot parse)


def mutate_bytes(data: bytearray, pos: int) -> bytearray:
    """Change the single byte at pos to a different printable ASCII char."""
    new_byte = random.choice(PRINTABLE_ASCII)
    while data[pos : pos + 1] == new_byte:  # ensure real change
        new_byte = random.choice(PRINTABLE_ASCII)
    mutated = bytearray(data)
    mutated[pos : pos + 1] = new_byte
    return mutated


def ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS mutations (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               file_path TEXT,
               mutation_pos INTEGER,
               original_text TEXT,
               mutated_text TEXT
           );"""
    )
    conn.commit()


def store_pair(
    conn: sqlite3.Connection,
    file_path: str,
    pos: int,
    original_text: str,
    mutated_text: str,
) -> None:
    conn.execute(
        "INSERT INTO mutations (file_path, mutation_pos, original_text, mutated_text) "
        "VALUES (?, ?, ?, ?)",
        (file_path, pos, original_text, mutated_text),
    )
    conn.commit()


def process_file(
    file_path: Path,
    validator: str,
    conn: sqlite3.Connection,
    max_attempts: int,
) -> None:
    data = file_path.read_bytes()
    if not data:
        return

    original_ok = run_validator(validator, file_path)
    if not original_ok:
        print(f"[skip] validator already fails on original: {file_path}")
        return

    print(f"[info] processing {file_path}")
    found_positions: Set[int] = set()
    attempts = 0

    while len(found_positions) < 10 and attempts < max_attempts:
        attempts += 1
        pos = random.randrange(len(data))
        if pos in found_positions or data[pos] == "\"":
            continue

        mutated_bytes = mutate_bytes(bytearray(data), pos)
        tmp_path = file_path.with_suffix(".tmp_mutate")
        tmp_path.write_bytes(mutated_bytes)

        if not run_validator(validator, tmp_path):
            # success – store pair
            store_pair(
                conn,
                str(file_path),
                pos,
                data.decode(errors="ignore"),
                mutated_bytes.decode(errors="ignore"),
            )
            found_positions.add(pos)
            print(f"  [✓] mutation #{len(found_positions)} at byte {pos}")
        tmp_path.unlink(missing_ok=True)

    if len(found_positions) < 10:
        print(f"  [✗] only {len(found_positions)} mutations found (needs 10)")


def traverse_and_mutate(
    folder: Path,
    validator: str,
    db_path: Path,
    max_attempts: int,
    seed: int | None = None,
) -> None:
    if seed is not None:
        random.seed(seed)

    with sqlite3.connect(db_path) as conn:
        ensure_table(conn)

        for path in folder.rglob("*"):
            if path.is_file():
                try:
                    process_file(path, validator, conn, max_attempts)
                except Exception as e:
                    print(f"[err] {path}: {e}", file=sys.stderr)


# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(description="Mutate files and store pairs")
    parser.add_argument("--folder", required=True, help="root folder to traverse")
    parser.add_argument("--validator", required=True, help="validator executable path")
    parser.add_argument("--database", required=True, help="SQLite output file (.sqlite)")
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=10_000,
        help="maximum mutation attempts per file (default 10000)",
    )
    parser.add_argument("--seed", type=int, help="RNG seed (optional)")
    args = parser.parse_args()

    traverse_and_mutate(
        Path(args.folder).resolve(),
        args.validator,
        Path(args.database).resolve(),
        args.max_attempts,
        args.seed,
    )
    print("[done] all files processed")


if __name__ == "__main__":
    main()