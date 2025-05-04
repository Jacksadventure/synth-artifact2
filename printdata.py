#!/usr/bin/env python3
"""
Generate all tables and metrics for the FSynth‑Artifact evaluation.

Changes vs. the original version
--------------------------------
* **Type‑safety:** every numeric column coming from SQLite is CAST to REAL.
* **Robust statistics:** a single `calc_stats()` helper silently skips
  NULLs / non‑numeric strings, so you never hit “unsupported operand types”.
* **Unified helpers:** all distance / ratio calculations call the same helpers,
  making the script easier to maintain.
"""

import sqlite3
import math
from typing import Dict, Tuple, List, Any

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

DATABASES = ["multiple.sqlite", "truncated.sqlite", "single.sqlite"]
DEFAULT_TIMEOUT = 240.0          # seconds – assumed when `repair_time` is NULL

# --------------------------------------------------------------------------- #
# Generic helpers
# --------------------------------------------------------------------------- #

def safe_float(v: Any) -> float | None:
    """Return `float(v)` or None if it cannot be parsed."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(v)
    except (ValueError, TypeError):
        return None

def calc_stats(values: List[Any]) -> Tuple[float, float]:
    """Mean & stdev, skipping NULL / non‑numeric entries."""
    nums = [safe_float(v) for v in values]
    nums = [x for x in nums if x is not None]
    n = len(nums)
    if n == 0:
        return 0.0, 0.0
    mean = sum(nums) / n
    stdev = math.sqrt(sum((x - mean) ** 2 for x in nums) / n) if n > 1 else 0.0
    return mean, stdev

# --------------------------------------------------------------------------- #
# Core Levenshtein with operation counts
# --------------------------------------------------------------------------- #

def edit_distance_with_ops(a: str, b: str) -> Tuple[int, int, int, int]:
    """Levenshtein distance + (delete, insert, replace) op counts."""
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    op = [[""]*(n+1) for _ in range(m+1)]

    for i in range(1, m+1):
        dp[i][0] = i
        op[i][0] = 'D'
    for j in range(1, n+1):
        dp[0][j] = j
        op[0][j] = 'I'

    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
                op[i][j] = 'M'
            else:
                del_cost = dp[i-1][j] + 1
                ins_cost = dp[i][j-1] + 1
                rep_cost = dp[i-1][j-1] + 1
                dp[i][j] = c = min(del_cost, ins_cost, rep_cost)
                op[i][j] = ('D' if c == del_cost else
                            'I' if c == ins_cost else
                            'R')

    dist = dp[m][n]
    del_c = ins_c = rep_c = 0
    i, j = m, n
    while i or j:
        match op[i][j]:
            case 'M':
                i, j = i-1, j-1
            case 'D':
                del_c += 1; i -= 1
            case 'I':
                ins_c += 1; j -= 1
            case 'R':
                rep_c += 1; i, j = i-1, j-1
    return dist, del_c, ins_c, rep_c

# --------------------------------------------------------------------------- #
# Table 4‑5 (General metrics)
# --------------------------------------------------------------------------- #

def calculate_and_display_detailed_metrics() -> None:
    combined: Dict[Tuple[str, str], Dict[str, list | int]] = {}

    for db in DATABASES:
        print(f"\nProcessing database: {db}")
        data: Dict[Tuple[str, str], Dict[str, list | int]] = {}
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    format,
                    algorithm,
                    CAST(distance_original_broken    AS REAL),
                    CAST(distance_broken_repaired   AS REAL),
                    CAST(distance_original_repaired AS REAL),
                    fixed = 1                      AS success,
                    CAST(IFNULL(repair_time, ?)    AS REAL)
                FROM results
            """, (DEFAULT_TIMEOUT,))
            for fmt, alg, dob, dbr, dor, succ, rtime in cur.fetchall():
                key = (fmt, alg)
                bucket = data.setdefault(key, {
                    "br": [], "or": [], "times": [],
                    "total": 0, "success": 0
                })
                bucket["total"] += 1
                bucket["times"].append(rtime)
                if succ:
                    bucket["br"].append(dbr)
                    bucket["or"].append(dor)
                    bucket["success"] += 1
                # merge into combined
                cb = combined.setdefault(key, {
                    "br": [], "or": [], "times": [],
                    "total": 0, "success": 0
                })
                cb["total"] += 1
                cb["times"].append(rtime)
                if succ:
                    cb["br"].append(dbr)
                    cb["or"].append(dor)
                    cb["success"] += 1

        _print_metric_table(data, f"Metrics for {db}")

    _print_metric_table(combined, "Combined Metrics Across All Databases")

def _print_metric_table(dataset, title):
    print(f"\n{title}")
    print("-"*130)
    header = ("Format", "Algorithm", "Avg BR", "Stdev BR", "Avg OR",
              "Stdev OR", "Avg Time", "Stdev Time", "Successes", "Total")
    print(f"{header[0]:<10} {header[1]:<10} {header[2]:<10} {header[3]:<11} "
          f"{header[4]:<10} {header[5]:<11} {header[6]:<12} {header[7]:<12} "
          f"{header[8]:<10} {header[9]:<10}")
    print("-"*130)
    for (fmt, alg), m in sorted(dataset.items()):
        avg_br, sd_br   = calc_stats(m["br"])
        avg_or, sd_or   = calc_stats(m["or"])
        avg_t,  sd_t    = calc_stats(m["times"])
        print(f"{fmt:<10} {alg:<10} {avg_br:<10.2f} {sd_br:<11.2f} "
              f"{avg_or:<10.2f} {sd_or:<11.2f} {avg_t:<12.2f} "
              f"{sd_t:<12.2f} {m['success']:<10} {m['total']:<10}")

# --------------------------------------------------------------------------- #
# Table 4‑5 (Surviving data ratio)
# --------------------------------------------------------------------------- #

def calculate_avg_surviving_data() -> None:
    for mode, col in [("OR", "original_text"), ("CR", "broken_text")]:
        results: Dict[str, Dict[str, list]] = {}

        for db in DATABASES:
            with sqlite3.connect(db) as conn:
                cur = conn.cursor()
                cur.execute(f"""
                    SELECT algorithm, {col}, repaired_text
                    FROM results
                    WHERE fixed = 1 AND repaired_text IS NOT NULL
                """)
                for alg, orig, rep in cur.fetchall():
                    L = len(orig)
                    _, deletions, _, _ = edit_distance_with_ops(orig, rep)
                    ratio = (L - deletions) / L if L else 0
                    results.setdefault(db, {}).setdefault(alg, []).append(ratio)

        print(f"\n Surviving Data Ratio ({mode})")
        for db, algs in results.items():
            print(f"\nResults for {db}:")
            print("-"*70)
            print(f"{'Algorithm':<15} {'Avg Ratio':<15} {'Stdev':<15} {'Count':<10}")
            print("-"*70)
            for alg, vals in algs.items():
                avg, sd = calc_stats(vals)
                print(f"{alg:<15} {avg:<15.4f} {sd:<15.4f} {len(vals):<10}")

# --------------------------------------------------------------------------- #
# Table 4‑5 (Levenshtein distances)
# --------------------------------------------------------------------------- #

def all_distances() -> None:
    data: Dict[str, Dict[str, List[float]]] = {}
    for db in DATABASES:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT algorithm,
                       CAST(distance_broken_repaired  AS REAL),
                       CAST(distance_original_repaired AS REAL)
                FROM results
                WHERE fixed = 1
            """)
            for alg, dbr, dor in cur.fetchall():
                bucket = data.setdefault(alg, {"br": [], "or": []})
                if dbr is not None:
                    bucket["br"].append(dbr)
                if dor is not None:
                    bucket["or"].append(dor)

    print("\nOverall Distance Metrics Across All Databases")
    print("-"*80)
    print(f"{'Algorithm':<15} {'Avg BR':<10} {'Stdev BR':<10} "
          f"{'Avg OR':<10} {'Stdev OR':<10}")
    print("-"*80)
    for alg, m in data.items():
        avg_br, sd_br = calc_stats(m["br"])
        avg_or, sd_or = calc_stats(m["or"])
        print(f"{alg:<15} {avg_br:<10.2f} {sd_br:<10.2f} "
              f"{avg_or:<10.2f} {sd_or:<10.2f}")

# --------------------------------------------------------------------------- #
# Table 6 (Count repaired)
# --------------------------------------------------------------------------- #

def count_fixed_files() -> None:
    totals: Dict[str, int] = {}
    for db in DATABASES:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT algorithm, COUNT(*)
                FROM results
                WHERE fixed = 1
                GROUP BY algorithm
            """)
            rows = cur.fetchall()
        print(f"\nResults for {db}:")
        print("-"*40)
        print(f"{'Algorithm':<15} {'Fixed Count':<15}")
        print("-"*40)
        for alg, cnt in rows:
            print(f"{alg:<15} {cnt:<15}")
            totals[alg] = totals.get(alg, 0) + cnt

    print("\nTotal Fixed Files Across All Databases:")
    print("-"*40)
    print(f"{'Algorithm':<15} {'Fixed Count':<15}")
    print("-"*40)
    for alg, cnt in totals.items():
        print(f"{alg:<15} {cnt:<15}")

# --------------------------------------------------------------------------- #
# Table 7 (Perfect repairs)
# --------------------------------------------------------------------------- #

def count_perfect_repairs_by_algorithm() -> None:
    for db in DATABASES:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT format, algorithm, COUNT(*)
                FROM results
                WHERE distance_original_repaired = 0
                GROUP BY format, algorithm
            """)
            rows = cur.fetchall()
        print(f"\nPerfect Repairs by Algorithm in {db}:")
        if rows:
            for fmt, alg, cnt in rows:
                print(f"  Format: {fmt:<8}  Algorithm: {alg:<10}  Perfect: {cnt}")
        else:
            print("  No perfect repairs found.")

# --------------------------------------------------------------------------- #
# Table 8 (Efficiency)  + iterations
# --------------------------------------------------------------------------- #

def calculate_avg_runtime_and_iterations() -> None:
    runtimes: Dict[str, float] = {}
    counts:   Dict[str, int]   = {}
    iterations: Dict[str, Tuple[int, float]] = {}  # total_count, total_iters

    for db in DATABASES:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()

            # Average runtime for *all* rows (incl. failures) to match old paper.
            cur.execute("""
                SELECT algorithm,
                       AVG(CAST(repair_time AS REAL)),
                       COUNT(*)
                FROM results
                GROUP BY algorithm
            """)
            for alg, avg_rt, cnt in cur.fetchall():
                runtimes[alg] = runtimes.get(alg, 0.0) + avg_rt * cnt
                counts[alg]   = counts.get(alg, 0)   + cnt

            # Iterations column is optional
            cur.execute("PRAGMA table_info(results)")
            if "iterations" in [c[1] for c in cur.fetchall()]:
                cur.execute("""
                    SELECT algorithm, COUNT(*), AVG(iterations)
                    FROM results
                    WHERE iterations > 0
                    GROUP BY algorithm
                """)
                for alg, cnt, avg_it in cur.fetchall():
                    tot_cnt, tot_it = iterations.get(alg, (0, 0.0))
                    iterations[alg] = (tot_cnt + cnt, tot_it + cnt*avg_it)

    # Print runtime
    print("\nOverall Average Runtime Across All Databases:")
    print("-"*50)
    print(f"{'Algorithm':<15} {'Avg Time (s)':<15} {'Count':<10}")
    print("-"*50)
    for alg in sorted(runtimes.keys()):
        avg_time = runtimes[alg] / counts[alg] if counts[alg] else 0
        print(f"{alg:<15} {avg_time:<15.2f} {counts[alg]:<10}")

    # Print iterations (if present)
    if iterations:
        print("\nAverage Iterations Across All Databases:")
        print("-"*50)
        print(f"{'Algorithm':<15} {'Total Count':<15} {'Avg Iter':<15}")
        print("-"*50)
        for alg, (tot_cnt, tot_iters) in iterations.items():
            print(f"{alg:<15} {tot_cnt:<15} {tot_iters/tot_cnt:<15.2f}")

# --------------------------------------------------------------------------- #
# Main driver
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    print("----------------Table 4‑5 (General)-------------------------------")
    calculate_and_display_detailed_metrics()

    print("----------------Table 4‑5 (Data Survive)--------------------------")
    calculate_avg_surviving_data()

    print("----------------Table 4‑5 (Levenshtein distances)-----------------")
    all_distances()

    print("----------------Table 6 (Count repaired)--------------------------")
    count_fixed_files()

    print("----------------Table 7 (Perfectly repaired entries)--------------")
    count_perfect_repairs_by_algorithm()

    print("----------------Table 8 (Efficiency & iterations)-----------------")
    calculate_avg_runtime_and_iterations()