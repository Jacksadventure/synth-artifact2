#!/usr/bin/env python3
"""
run_repairs_resume.py – 可断点续跑的批量修复基准脚本
----------------------------------------------------
1. 每个源库最多取 N 条原始行；默认 N=1000。
2. 四种算法并行写入同一张 results 表；
   若脚本意外中断，可再次运行，它会 **跳过 repair_time>0 的已完成行**。
"""

from __future__ import annotations
import argparse, os, random, re, sqlite3, subprocess, textwrap, time
from pathlib import Path
from typing import Iterable, List, Tuple

# ──────────────────────── Configuration ───────────────────────── #
ALL_MUTATION_DBS = {
    "dot":  "double_dot.db",
    "json": "double_json.db",
    "ini":  "double_ini.db",
    "lisp": "double_lisp.db",
    "obj":  "double_obj.db",
}
DEFAULT_ROWS   = 1_000
RESULT_DB      = "result10.db"
REPAIR_ALGORITHMS = ["DDMax", "erepair", "DDMaxG", "Antlr"]

PROJECT_PATHS = {
    "json": "/Users/jack/fsynth-artifact/project/bin/subjects/cjson/cjson",
    "ini":  "/Users/jack/fsynth-artifact/project/bin/subjects/ini/ini",
    "lisp": "/Users/jack/fsynth-artifact/project/bin/subjects/sexp-parser/sexp",
    "dot":  "/Users/jack/fsynth-artifact/project/bin/subjects/dot/build/dot_parser",
    "obj":  "/Users/jack/fsynth-artifact/obj/build/obj_parser"
}

VALIDATION_TIMEOUT = 30
REPAIR_TIMEOUT     = 20
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

# ───────────────────────── DB helpers ──────────────────────────── #

def create_results_db(path: str) -> None:
    """新建 results 表；若已存在则保持字段一致"""
    conn = sqlite3.connect(path)
    conn.execute(textwrap.dedent("""
        CREATE TABLE IF NOT EXISTS results(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            format TEXT, file_id INTEGER, corrupted_index INTEGER, algorithm TEXT,
            original_text TEXT, broken_text TEXT, repaired_text TEXT DEFAULT '',
            fixed INTEGER DEFAULT 0, iterations INTEGER DEFAULT 0,
            repair_time REAL DEFAULT 0.0,
            correct_runs INTEGER DEFAULT 0, incorrect_runs INTEGER DEFAULT 0,
            incomplete_runs INTEGER DEFAULT 0,
            distance_original_broken INTEGER DEFAULT 0,
            distance_broken_repaired  INTEGER DEFAULT 0,
            distance_original_repaired INTEGER DEFAULT 0,
            UNIQUE(format,file_id,corrupted_index,algorithm)
        )
    """))
    conn.commit()
    conn.close()

# ───────────────────────── Text helpers ───────────────────────── #

def lev(a: str, b: str) -> int:
    if a == b:          return 0
    if not a:           return len(b)
    if not b:           return len(a)
    prev = list(range(len(b) + 1))
    for ca in a:
        cur = [prev[0] + 1]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[-1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

# ───────────────────── Load & insert samples ───────────────────── #

def load_mutations(limit: int, mutation_dbs: dict) -> Iterable[Tuple]:
    for fmt, db in mutation_dbs.items():
        if not os.path.exists(db):
            print(f"[WARN] {db} missing; skip format '{fmt}'")
            continue
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM mutations ORDER BY id ASC LIMIT ?", (limit,))
        rows = [r for r in cur.fetchall()]
        conn.close()
        print(f"[LOAD] {fmt}: kept {len(rows)} / {limit} rows")
        for idx, r in enumerate(rows, 1):
            yield (
                r["id"], fmt, r["file_path"], idx, r["original_text"], r["mutated_text"],
            )

def insert_samples(samples: List[Tuple], db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM results")
    if cur.fetchone()[0]:         
        print("[SKIP] results table already contains rows – skip insertion")
        conn.close()
        return
    # ─────────────────────────────────────────────────────

    new_rows = 0
    for sid, fmt, fpath, idx, orig, mut in samples:
        fid = abs(hash(fpath)) % (10 ** 9)
        for alg in REPAIR_ALGORITHMS:
            cur.execute(
                """INSERT OR IGNORE INTO results(
                       format,file_id,corrupted_index,algorithm,
                       original_text,broken_text)
                   VALUES (?,?,?,?,?,?)""",
                (fmt, fid, idx, alg, orig, mut))
            if cur.rowcount:
                new_rows += 1
    conn.commit()
    conn.close()
    print(f"[INSERT] {new_rows} new rows inserted")

# ───────────────────── Repair helpers ─────────────────────────── #

def validate(path: str, fmt: str) -> bool:
    exe = PROJECT_PATHS.get(fmt)
    try:
        res = subprocess.run([exe, path], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=VALIDATION_TIMEOUT)
        return res.returncode == 0
    except Exception:
        return False

def oracle_info(out: bytes) -> Tuple[int,int,int,int]:
    txt = out.decode(errors="ignore")
    m = re.search(r"oracle runs: (\d+) correct: (\d+) incorrect: (\d+) incomplete: (\d+)", txt)
    return tuple(map(int, m.groups())) if m else (0,0,0,0)

def repair_and_update(cur: sqlite3.Cursor, conn: sqlite3.Connection,
                      row: sqlite3.Row, idx:int, total:int) -> None:
    (rid, fmt, fid, cidx, alg, orig, broken, rep, fixed, *_rest) = row
    infile  = f"tmp_{rid}_{random.randint(0,9999)}.{fmt}"
    outfile = Path(REPAIR_OUTPUT_DIR) / f"rep_{rid}.{fmt}"
    Path(infile).write_text(broken, encoding="utf-8")

    cmd = [a.format(infile=infile, outfile=str(outfile),
                    fmt_exe=PROJECT_PATHS.get(fmt, "")) for a in ALGORITHM_CMDS[alg]]
    dist_ob = lev(orig, broken)
    dist_br = dist_or = -1
    iters = cor = incor = incom = 0
    elapsed = 0.0
    try:
        start = time.time()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = proc.communicate(timeout=REPAIR_TIMEOUT)
        elapsed = time.time() - start
        iters,cor,incor,incom = oracle_info(stdout)
        if proc.returncode==0 and outfile.exists():
            rep = outfile.read_text(encoding="utf-8", errors="ignore")
            if validate(str(outfile), fmt):
                fixed = 1
            dist_br = lev(broken, rep)
            dist_or = lev(orig, rep)
    except subprocess.TimeoutExpired:
        elapsed = REPAIR_TIMEOUT
        print(f"[TIMEOUT] row {rid}")
    finally:
        for p in (infile, outfile):
            try: os.remove(p)
            except FileNotFoundError: pass

    print(f"[{idx:04}/{total}] {fmt:<4} {alg:<6} fixed={fixed} t={elapsed:4.1f}s")
    cur.execute(textwrap.dedent("""\
        UPDATE results SET repaired_text=?, fixed=?, iterations=?, repair_time=?,
               correct_runs=?, incorrect_runs=?, incomplete_runs=?,
               distance_original_broken=?, distance_broken_repaired=?,
               distance_original_repaired=? WHERE id=?"""),
        (rep, fixed, iters, elapsed, cor, incor, incom,
         dist_ob, dist_br, dist_or, rid))
    conn.commit()

def run_repairs(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM results WHERE repair_time=0")
    pending = cur.fetchone()[0]
    print(f"[REPAIR] {pending} pending rows (repair_time=0)")
    if not pending:
        conn.close()
        return

    cur.execute("SELECT * FROM results WHERE repair_time=0")
    rows = cur.fetchall()
    total = len(rows)
    for i, r in enumerate(rows, 1):
        repair_and_update(cur, conn, r, i, total)
    conn.close()

# ─────────────────────────── CLI ─────────────────────────────── #

def main() -> None:
    p = argparse.ArgumentParser(
        description="Resume-safe benchmark runner for multiple repair algorithms")
    p.add_argument('-f','--formats', nargs='+',
                   choices=list(ALL_MUTATION_DBS.keys()), default=['dot'],
                   help="Formats to process (default: dot)")
    p.add_argument('-o','--result-db', default=RESULT_DB,
                   help="SQLite DB to record results")
    p.add_argument('-n','--rows', type=int, default=DEFAULT_ROWS,
                   help="Original rows to pull from each mutation DB (default: 1000)")
    args = p.parse_args()

    mutation_dbs = {fmt: ALL_MUTATION_DBS[fmt] for fmt in args.formats}

    create_results_db(args.result_db)
    samples = list(load_mutations(args.rows, mutation_dbs))
    insert_samples(samples, args.result_db)
    run_repairs(args.result_db)

if __name__ == "__main__":
    main()