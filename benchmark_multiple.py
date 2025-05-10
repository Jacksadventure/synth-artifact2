#!/usr/bin/env python3
"""
run_repairs_verbose.py  –  skip non‑English originals, CLI format selection and output DB
"""

import os
import random
import re
import sqlite3
import subprocess
import time
import textwrap
import argparse
from pathlib import Path

# ─────────────── Configuration ─────────── #
ALL_MUTATION_DBS = {
    "dot":  "double_dot.db",
    "json": "double_json.db",
    "ini":  "double_ini.db",
    "lisp": "double_lisp.db",
    "obj":  "double_obj.db",
}
MAX_ORIGINALS_PER_DB = 100
DEFAULT_RESULT_DB = "result11.db"
REPAIR_ALGORITHMS = ["DDMax", "erepair", "DDMaxG", "Antlr"]

PROJECT_PATHS = {
    "json": "/Users/jack/fsynth-artifact/project/bin/subjects/cjson/cjson",
    "ini":  "/Users/jack/fsynth-artifact/project/bin/subjects/ini/ini",
    "lisp": "/Users/jack/fsynth-artifact/project/bin/subjects/sexp-parser/sexp",
    "dot":  "/Users/jack/fsynth-artifact/project/bin/subjects/dot/build/dot_parser",
    "obj":  "/Users/jack/fsynth-artifact/obj/build/obj_parser"
}

VALIDATION_TIMEOUT = 30
REPAIR_TIMEOUT     = 100
REPAIR_OUTPUT_DIR  = "repair_results"
os.makedirs(REPAIR_OUTPUT_DIR, exist_ok=True)

ALGORITHM_CMDS = {
    "erepair": ["./erepair", "{fmt_exe}", "{infile}", "{outfile}"],
    "DDMax":   ["java", "-jar", "./project/bin/erepair.jar", "-r", "-a", "DDMax",
                 "-i", "{infile}", "-o", "{outfile}"],
    "DDMaxG":  ["java", "-jar", "./project/bin/erepair.jar", "-r", "-a", "DDMaxG",
                 "-i", "{infile}", "-o", "{outfile}"],
    "Antlr":   ["java", "-jar", "./project/bin/erepair.jar", "-r", "-a", "Antlr",
                 "-i", "{infile}", "-o", "{outfile}"],
}

# ─────────────── Utility functions ─────────── #
def create_results_db(path: str):
    conn = sqlite3.connect(path)
    conn.execute("""CREATE TABLE IF NOT EXISTS results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        format TEXT, file_id INTEGER, corrupted_index INTEGER, algorithm TEXT,
        original_text TEXT, broken_text TEXT, repaired_text TEXT, fixed INTEGER,
        iterations INTEGER, repair_time REAL,
        correct_runs INTEGER, incorrect_runs INTEGER, incomplete_runs INTEGER,
        distance_original_broken INTEGER, distance_broken_repaired INTEGER,
        distance_original_repaired INTEGER);""")
    conn.commit()
    conn.close()


def lev(a: str, b: str) -> int:
    if a == b: return 0
    if not a: return len(b)
    if not b: return len(a)
    prev = list(range(len(b)+1))
    for ca in a:
        cur = [prev[0] + 1]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j]+1, cur[-1]+1, prev[j-1]+(ca!=cb)))
        prev = cur
    return prev[-1]


def is_ascii(s: str) -> bool:
    return all(ord(c) < 128 for c in s)


def load_mutations(max_orig: int, dbs: dict):
    for fmt, db in dbs.items():
        if not os.path.exists(db):
            print(f"[WARN] DB {db} missing for format '{fmt}'"); continue
        conn = sqlite3.connect(db);
        conn.row_factory = sqlite3.Row
        cur = conn.cursor(); cur.execute("SELECT * FROM mutations ORDER BY id ASC")
        seen, kept = set(), []
        for row in cur.fetchall():
            fp = row["file_path"]
            if fp in seen: continue
            if not is_ascii(row["original_text"]): continue
            seen.add(fp); kept.append(row)
            if len(kept) >= max_orig: break
        conn.close()
        print(f"[LOAD] {fmt}: kept {len(kept)} english originals")
        for idx, r in enumerate(kept, 1):
            snip = textwrap.shorten(r["original_text"].replace("\n", "\\n"), 70)
            print(f"   └─ {idx:03d} {Path(r['file_path']).name} | {snip}")
            yield (r["id"], fmt, r["file_path"], idx, r["original_text"], r["mutated_text"])


def insert_samples(samples, db_path):
    conn = sqlite3.connect(db_path); cur = conn.cursor(); count = 0
    for _, fmt, fpath, idx, orig, mut in samples:
        fid = abs(hash(fpath)) % (10**9)
        for alg in REPAIR_ALGORITHMS:
            cur.execute("""INSERT INTO results(
                format, file_id, corrupted_index, algorithm,
                original_text, broken_text,
                repaired_text, fixed, iterations, repair_time,
                correct_runs, incorrect_runs, incomplete_runs,
                distance_original_broken, distance_broken_repaired,
                distance_original_repaired)
                VALUES (?,?,?,?,?,?, '',0,0,0.0,0,0,0,0,0,0)""",
                (fmt, fid, idx, alg, orig, mut))
            count += 1
    conn.commit(); conn.close()
    print(f"[INSERT] {count} rows inserted")


def validate(path: str, fmt: str) -> bool:
    exe = PROJECT_PATHS.get(fmt)
    try:
        res = subprocess.run([exe, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=VALIDATION_TIMEOUT)
        return res.returncode == 0
    except Exception:
        return False


def oracle_info(out: bytes):
    txt = out.decode("utf-8", errors="ignore")
    m = re.search(r"oracle runs: (\d+) correct: (\d+) incorrect: (\d+) incomplete: (\d+)", txt)
    return tuple(map(int, m.groups())) if m else (0, 0, 0, 0)


def repair_and_update(cur, conn, row, idx, total):
    (rid, fmt, _, _, alg, orig, broken, rep, fixed, *_) = row
    infile = f"tmp_{rid}_{random.randint(0,9999)}.{fmt}"
    outfile = os.path.join(REPAIR_OUTPUT_DIR, f"rep_{rid}.{fmt}")
    Path(infile).write_text(broken, encoding="utf-8")

    cmd = [c.format(infile=infile, outfile=outfile, fmt_exe=PROJECT_PATHS.get(fmt, ""))
           for c in ALGORITHM_CMDS[alg]]
    dist_ob = lev(orig, broken); dist_br = dist_or = -1
    iters = cor = incor = incom = 0; elapsed = 0.0
    try:
        start = time.time()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = proc.communicate(timeout=REPAIR_TIMEOUT)
        elapsed = time.time() - start
        iters, cor, incor, incom = oracle_info(out)
        if proc.returncode == 0 and os.path.exists(outfile):
            rep = Path(outfile).read_text(encoding="utf-8", errors="ignore")
            if validate(outfile, fmt): fixed = 1
            dist_br = lev(broken, rep); dist_or = lev(orig, rep)
    except subprocess.TimeoutExpired:
        elapsed = REPAIR_TIMEOUT; print(f"[{rid}] TIMEOUT")
    finally:
        for p in (infile, outfile):
            if os.path.exists(p): os.remove(p)

    print(f"[{idx:04}/{total}] {fmt} {alg} fixed={fixed} t={elapsed:.1f}s")
    cur.execute("""UPDATE results SET repaired_text=?, fixed=?, iterations=?, repair_time=?,
                   correct_runs=?, incorrect_runs=?, incomplete_runs=?,
                   distance_original_broken=?, distance_broken_repaired=?, distance_original_repaired=?
                   WHERE id=?""",
                (rep, fixed, iters, elapsed, cor, incor, incom, dist_ob, dist_br, dist_or, rid))
    conn.commit()


def run_repairs(db_path):
    conn = sqlite3.connect(db_path); cur = conn.cursor()
    cur.execute("SELECT * FROM results"); rows = cur.fetchall()
    print(f"[REPAIR] total {len(rows)} rows")
    for i, row in enumerate(rows, 1): repair_and_update(cur, conn, row, i, len(rows))
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Run repairs on mutated inputs with optional formats and DB path.")
    parser.add_argument('-f', '--formats', nargs='+', choices=list(ALL_MUTATION_DBS.keys()),
                        default=['dot'], help="Formats to process (default: ['dot'])")
    parser.add_argument('-o', '--result-db', default=DEFAULT_RESULT_DB,
                        help="Path to the results database (default: result11.db)")
    args = parser.parse_args()

    selected_dbs = {fmt: ALL_MUTATION_DBS[fmt] for fmt in args.formats}
    create_results_db(args.result_db)
    samples = list(load_mutations(MAX_ORIGINALS_PER_DB, selected_dbs))
    insert_samples(samples, args.result_db)
    run_repairs(args.result_db)

if __name__ == "__main__":
    main()
