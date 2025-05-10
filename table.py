#!/usr/bin/env python3
import argparse
import sqlite3
import math
import statistics
from collections import defaultdict
from typing import Dict, List, Tuple

DATABASES = ["double.db", "truncated.db", "single.db"]
DEFAULT_TIMEOUT = 240.0  # fallback repair_time

def safe_int(x):
    try:    return int(x)
    except: return None

def calculate_and_display_detailed_metrics():
    """
    TABLE 4–5 General Metrics: per-DB and combined
    """
    combined = defaultdict(lambda: {
        "broken_repaired": [], "original_repaired": [],
        "times": [], "succ_times": [], "total": 0, "succ": 0
    })

    for db in DATABASES:
        print(f"\n--- Metrics for {db} ---")
        conn = sqlite3.connect(db)
        cur  = conn.cursor()
        cur.execute(f"""
            SELECT format, algorithm,
                   distance_original_broken,
                   distance_broken_repaired,
                   distance_original_repaired,
                   fixed,
                   IFNULL(repair_time, ?)
              FROM results
        """, (DEFAULT_TIMEOUT,))
        per_db = {}
        for fmt, alg, dob, dbr, dor, fixed, rt in cur.fetchall():
            key = (fmt,alg)
            dob_i = safe_int(dob)
            dbr_i = safe_int(dbr)
            dor_i = safe_int(dor)
            fixed_i= safe_int(fixed) or 0
            per_db.setdefault(key, {
                "broken_repaired":[], "original_repaired":[],
                "times":[], "succ_times":[], "total":0, "succ":0
            })
            rec = per_db[key]
            rec["total"] += 1
            rec["times"].append(float(rt))
            if fixed_i==1:
                rec["broken_repaired"].append(dbr_i)
                rec["original_repaired"].append(dor_i)
                rec["succ_times"].append(float(rt))
                rec["succ"] += 1
            # merge into combined
            c = combined[key]
            c["total"] += 1
            c["times"].append(float(rt))
            if fixed_i==1:
                c["broken_repaired"].append(dbr_i)
                c["original_repaired"].append(dor_i)
                c["succ_times"].append(float(rt))
                c["succ"] += 1

        conn.close()
        display_metrics(per_db, header=f"Detailed Metrics for {db}")

    display_metrics(combined, header="Combined Metrics Across All DBs")

def display_metrics(data, header="Metrics"):
    print(f"\n{header}")
    print("-"*110)
    cols = ("Format","Algorithm","Avg BR","σ BR","Avg OR","σ OR","Avg Time","σ Time","Recovery","Total")
    print(" | ".join(f"{c:<12}" for c in cols))
    print("-"*110)
    for (fmt,alg), rec in sorted(data.items()):
        br, or_, tt, st = rec["broken_repaired"], rec["original_repaired"], rec["times"], rec["succ_times"]
        mean_br = statistics.mean(br) if br else 0
        sd_br   = statistics.pstdev(br) if len(br)>1 else 0
        mean_or = statistics.mean(or_) if or_ else 0
        sd_or   = statistics.pstdev(or_) if len(or_)>1 else 0
        mean_t  = statistics.mean(st) if st else 0
        sd_t    = statistics.pstdev(st) if len(st)>1 else 0
        rec_rate= (rec["succ"]/rec["total"]*100) if rec["total"] else 0
        print(f"{fmt:<12} | {alg:<12} | "
              f"{mean_br:>7.1f} | {sd_br:>7.1f} | "
              f"{mean_or:>7.1f} | {sd_or:>7.1f} | "
              f"{mean_t:>8.2f} | {sd_t:>8.2f} | "
              f"{rec_rate:>8.1f}% | {rec['total']:>5}")

def calculate_avg_surviving_data():
    """
    TABLE 4–5 Data Survive: fraction of input preserved
    """
    def stats(vals):
        mean = statistics.mean(vals) if vals else 0
        sd   = statistics.pstdev(vals) if len(vals)>1 else 0
        return mean, sd

    for mode, col in [("OR","original_text"),("BR","broken_text")]:
        print(f"\n--- Surviving Data Ratio ({mode}) ---")
        for db in DATABASES:
            ratios = defaultdict(list)
            conn = sqlite3.connect(db); cur = conn.cursor()
            cur.execute(f"""
                SELECT algorithm, {col}, repaired_text
                  FROM results WHERE fixed=1 AND repaired_text IS NOT NULL
            """)
            for alg, orig, rep in cur.fetchall():
                L = len(orig or "")
                dist,_,_,_ = edit_distance_with_ops(orig, rep)
                ratio = (L - dist)/L if L>0 else 0
                ratios[alg].append(ratio)
            conn.close()
            print(f"\n{db}")
            for alg, vals in ratios.items():
                mn, sd = stats(vals)
                print(f"  {alg:<10} Avg={mn:.3f}, σ={sd:.3f}, N={len(vals)}")

def all_distances():
    """
    TABLE 4–5 Levenshtein: overall avg±σ of both distances, fixed=1 only
    """
    data = defaultdict(lambda: {"BR":[], "OR":[]})
    for db in DATABASES:
        conn = sqlite3.connect(db); cur = conn.cursor()
        cur.execute("""
            SELECT algorithm, distance_broken_repaired, distance_original_repaired
              FROM results WHERE fixed=1
        """)
        for alg, dbr, dor in cur.fetchall():
            dbr_i = safe_int(dbr)
            dor_i = safe_int(dor)
            if dbr_i is not None: data[alg]["BR"].append(dbr_i)
            if dor_i is not None: data[alg]["OR"].append(dor_i)
        conn.close()
    print("\n--- Overall Distance Metrics ---")
    print("Algorithm | Avg BR σBR | Avg OR σOR")
    for alg, rec in data.items():
        mn_br = statistics.mean(rec["BR"]) if rec["BR"] else 0
        sd_br = statistics.pstdev(rec["BR"]) if len(rec["BR"])>1 else 0
        mn_or = statistics.mean(rec["OR"]) if rec["OR"] else 0
        sd_or = statistics.pstdev(rec["OR"]) if len(rec["OR"])>1 else 0
        print(f"{alg:<10} | {mn_br:>6.1f} {sd_br:>6.1f} | {mn_or:>6.1f} {sd_or:>6.1f}")

def count_fixed_files():
    """
    TABLE 6: count fixed=1 per algorithm, per DB and total
    """
    total = defaultdict(int)
    for db in DATABASES:
        conn = sqlite3.connect(db); cur = conn.cursor()
        cur.execute("SELECT algorithm, COUNT(*) FROM results WHERE fixed=1 GROUP BY algorithm")
        print(f"\n{db}")
        for alg, cnt in cur.fetchall():
            total[alg] += cnt
            print(f"  {alg:<10}: {cnt}")
        conn.close()
    print("\nTotal fixed across all DBs:")
    for alg, cnt in total.items():
        print(f"  {alg:<10}: {cnt}")

def count_perfect_repairs():
    """
    TABLE 7: perfect repairs (distance_original_repaired=0 & fixed=1)
    """
    for db in DATABASES:
        conn = sqlite3.connect(db); cur = conn.cursor()
        cur.execute("""
            SELECT algorithm, COUNT(*) FROM results
             WHERE fixed=1 AND distance_original_repaired=0
             GROUP BY algorithm
        """)
        print(f"\nPerfect in {db}")
        for alg, cnt in cur.fetchall():
            print(f"  {alg:<10}: {cnt}")
        conn.close()

def calculate_avg_runtime_iterations():
    """
    TABLE 8: avg repair_time & avg iterations for fixed=1
    """
    total_time = defaultdict(float)
    total_iter = defaultdict(int)
    total_cnt  = defaultdict(int)

    for db in DATABASES:
        conn = sqlite3.connect(db); cur = conn.cursor()
        cur.execute("""
            SELECT algorithm, AVG(repair_time), AVG(iterations), COUNT(*)
              FROM results WHERE fixed=1 GROUP BY algorithm
        """)
        print(f"\n{db} Avg runtime & iterations")
        for alg, avg_rt, avg_it, cnt in cur.fetchall():
            print(f"  {alg:<10} time={avg_rt:.2f}s iters={avg_it:.1f} N={cnt}")
            total_time[alg] += (avg_rt or 0) * cnt
            total_iter[alg] += (avg_it or 0) * cnt
            total_cnt[alg]  += cnt
        conn.close()

    print("\nOverall Avg (weighted)")
    for alg in total_cnt:
        avg_rt = total_time[alg] / total_cnt[alg]
        avg_it = total_iter[alg] / total_cnt[alg]
        print(f"  {alg:<10} time={avg_rt:.2f}s iters={avg_it:.1f} N={total_cnt[alg]}")

def edit_distance_with_ops(strA: str, strB: str) -> Tuple[int,int,int,int]:
    m, n = len(strA), len(strB)
    dp  = [[0]*(n+1) for _ in range(m+1)]
    op  = [[None]*(n+1) for _ in range(m+1)]
    for i in range(1,m+1):
        dp[i][0]=i; op[i][0]='D'
    for j in range(1,n+1):
        dp[0][j]=j; op[0][j]='I'
    for i in range(1,m+1):
        for j in range(1,n+1):
            if strA[i-1]==strB[j-1]:
                dp[i][j]=dp[i-1][j-1]; op[i][j]='M'
            else:
                dc,ic,rc = dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+1
                dp[i][j]=min(dc,ic,rc)
                op[i][j] = 'D' if dp[i][j]==dc else ('I' if dp[i][j]==ic else 'R')
    dist=dp[m][n]; di,ii,ri=0,0,0
    i,j=m,n
    while i>0 or j>0:
        o=op[i][j]
        if o=='M': i,j=i-1,j-1
        elif o=='D': di+=1; i-=1
        elif o=='I': ii+=1; j-=1
        elif o=='R': ri+=1; i,j=i-1,j-1
        else: break
    return dist, di, ii, ri

if __name__=="__main__":
    print("---------------- Table 4–5 General Metrics ----------------")
    calculate_and_display_detailed_metrics()
    print("\n---------------- Table 4–5 Data Survive ----------------")
    calculate_avg_surviving_data()
    print("\n---------------- Table 4–5 Distances ----------------")
    all_distances()
    print("\n---------------- Table 6: Fixed Counts ----------------")
    count_fixed_files()
    print("\n---------------- Table 7: Perfect Repairs ----------------")
    count_perfect_repairs()
    print("\n---------------- Table 8: Runtime & Iterations ---------")
    calculate_avg_runtime_iterations()