#!/usr/bin/env python3
"""
mutate_and_store.py  (two-byte mutation, only need one)
-------------------------------------------------------
Traverse folder, mutate each file by changing **two distinct byte positions**
at once.  If the mutated file makes the external validator fail, store that
(original_text, mutated_text, "pos1,pos2") into SQLite.  Only ONE such pair
per original file is required.

Example
-------
python mutate_and_store.py \
       --folder  ./data \
       --validator /usr/local/bin/ini-linter \
       --database mutations.sqlite
"""

import argparse, os, random, sqlite3, string, subprocess, sys
from pathlib import Path
from typing import Tuple

PRINTABLE_ASCII = [c.encode() for c in string.printable if c not in ("\n", "\r")]

# ─────────────────────────── helpers ────────────────────────────────────────
def run_validator(exe: str, path: Path) -> bool:
    try:
        res = subprocess.run([exe, str(path)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             timeout=10)
        return res.returncode == 0
    except Exception:
        return False

def mutate_two_positions(data: bytearray, p1: int, p2: int) -> bytearray:
    """Return a copy where byte at p1 and p2 are changed to random printable ones."""
    out = bytearray(data)
    for pos in (p1, p2):
        new_b = random.choice(PRINTABLE_ASCII)
        while out[pos:pos+1] == new_b:
            new_b = random.choice(PRINTABLE_ASCII)
        out[pos:pos+1] = new_b
    return out

def ensure_table(conn: sqlite3.Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS mutations (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               file_path TEXT,
               mutation_pos TEXT,            -- "p1,p2"
               original_text TEXT,
               mutated_text TEXT
           )"""
    ); conn.commit()

def store_pair(conn: sqlite3.Connection, fpath: str,
               pos_pair: Tuple[int, int], orig: str, mut: str):
    conn.execute(
        "INSERT INTO mutations (file_path, mutation_pos, original_text, mutated_text) "
        "VALUES (?, ?, ?, ?)",
        (fpath, f"{pos_pair[0]},{pos_pair[1]}", orig, mut),
    ); conn.commit()

# ────────────────────────── core logic ──────────────────────────────────────
def process_file(path: Path, validator: str,
                 conn: sqlite3.Connection, max_attempts: int):
    data = path.read_bytes()
    if not data: return

    if not run_validator(validator, path):
        print(f"[skip] original already invalid: {path}"); return

    print(f"[info] processing {path}")
    attempts = 0
    success  = False

    while not success and attempts < max_attempts:
        attempts += 1
        p1, p2 = random.sample(range(len(data)), 2)   # two distinct positions
        if data[p1] == "\"" or data[p2] == "\"":
            continue
        mutated = mutate_two_positions(bytearray(data), p1, p2)

        tmp = path.with_suffix(".tmp_mut")
        tmp.write_bytes(mutated)

        if not run_validator(validator, tmp):
            store_pair(conn, str(path), (p1, p2),
                       data.decode(errors="ignore"),
                       mutated.decode(errors="ignore"))
            print(f"  [✓] mutation at ({p1},{p2}) caused failure")
            success = True
        tmp.unlink(missing_ok=True)

    if not success:
        print("  [✗] no failing mutation found within max_attempts")

def traverse(folder: Path, validator: str, db: Path,
             max_attempts: int, seed: int | None):
    if seed is not None:
        random.seed(seed)

    with sqlite3.connect(db) as conn:
        ensure_table(conn)
        for file in folder.rglob("*"):
            if file.is_file():
                try:
                    process_file(file, validator, conn, max_attempts)
                except Exception as e:
                    print(f"[err] {file}: {e}", file=sys.stderr)

# ───────────────────────────────── main ─────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Two-byte mutate & store")
    ap.add_argument("--folder", required=True)
    ap.add_argument("--validator", required=True)
    ap.add_argument("--database", required=True)
    ap.add_argument("--max-attempts", type=int, default=10_000)
    ap.add_argument("--seed", type=int)
    args = ap.parse_args()

    traverse(Path(args.folder).resolve(),
             args.validator,
             Path(args.database).resolve(),
             args.max_attempts,
             args.seed)
    print("[done] all files processed")

if __name__ == "__main__":
    main()