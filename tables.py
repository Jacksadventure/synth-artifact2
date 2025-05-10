#!/usr/bin/env python3
"""
tables.py

Generate TABLES III–VIII from three SQLite DBs:
  --single    single-byte corruptions
  --double    double-byte corruptions
  --truncated truncated inputs

Each DB must have a `results` table with:
    format TEXT,
    original_text TEXT,
    distance_broken_repaired INTEGER,
    distance_original_repaired INTEGER,
    fixed INTEGER,
    iterations INTEGER,
    repair_time REAL,
    algorithm TEXT
"""

import argparse, sqlite3, statistics
from collections import defaultdict
from typing import Dict, List, Tuple

def safe_int(x):
    try:    return int(x)
    except: return None

def print_table_iii(single_db, double_db, trunc_db):
    # TABLE III: counts & record-length mean±σ in single_db
    def load_counts(db):
        c = sqlite3.connect(db).cursor()
        c.execute("SELECT format, COUNT(*) FROM results GROUP BY format")
        d = {fmt:cnt for fmt,cnt in c.fetchall()}
        c.connection.close()
        return d

    def load_lengths(db):
        c = sqlite3.connect(db).cursor()
        c.execute("SELECT format, LENGTH(original_text) FROM results")
        d: Dict[str,List[int]] = {}
        for fmt, L in c.fetchall():
            d.setdefault(fmt, []).append(L)
        c.connection.close()
        return d

    sc = load_counts(single_db)
    dc = load_counts(double_db)
    tc = load_counts(trunc_db)
    lengths = load_lengths(single_db)
    fmts = sorted(set(sc)|set(dc)|set(tc))

    hdr = ["Format","Record Len.","Single Corr.","Double Corr.","Truncated"]
    widths = {h:len(h) for h in hdr}
    rows = []
    for f in fmts:
        lens = lengths.get(f,[])
        if lens:
            m = statistics.mean(lens); s = statistics.pstdev(lens)
            rec = f"{m:.1f} σ {s:.1f}"
        else:
            rec = "N/A"
        sct, dct, tct = sc.get(f,0), dc.get(f,0), tc.get(f,0)
        pct = (tct*100/sct) if sct else 0.0
        tr = f"{tct} ({pct:.1f}%)"
        row = [f.upper(), rec, str(sct), str(dct), tr]
        rows.append(row)
        for h,cell in zip(hdr,row):
            widths[h] = max(widths[h], len(cell))

    print("\n**TABLE III: Number of corrupt inputs**\n")
    print("| " + " | ".join(h.ljust(widths[h]) for h in hdr) + " |")
    print("|-" + "-|-".join("-"*widths[h] for h in hdr) + "-|")
    for r in rows:
        print("| " + " | ".join(r[i].ljust(widths[hdr[i]]) for i in range(len(hdr))) + " |")

def print_table_iv(single_db: str, double_db: str, trunc_db: str):
    # TABLE IV: distance_broken_repaired mean±σ for fixed=1, plus avg & recovery
    scenarios = [("Single", single_db), ("Double", double_db), ("Truncated", trunc_db)]
    algs   = ["erepair","DDMax","DDMaxG","Antlr"]
    labels = {"erepair":"εREPAIR","DDMax":"DDMax","DDMaxG":"DDMaxG","Antlr":"ANTLR"}

    print("\n**TABLE IV: Distance between corrupt data and repaired data**\n")
    # collect for avg & recovery
    agg_vals = {alg:[] for alg in algs}
    agg_flags = {alg:[] for alg in algs}

    for name, db in scenarios:
        conn = sqlite3.connect(db); cur = conn.cursor()
        cur.execute("""
            SELECT format, algorithm, distance_broken_repaired, fixed
              FROM results
        """)
        data: Dict[Tuple[str,str], List[int]] = {}
        for fmt, alg, dist, fixed in cur.fetchall():
            di = safe_int(dist)
            fi = safe_int(fixed)
            # recovery collects all flags
            if fi is not None:
                agg_flags[alg].append(fi)
            # distance collects only fixed=1
            if di is not None and fi == 1:
                data.setdefault((str(fmt), alg), []).append(di)
                agg_vals[alg].append(di)
        conn.close()

        fmts = sorted({fmt for fmt,_ in data})
        if not fmts:
            continue

        # compute column widths
        fmt_max = max((len(f) for f in fmts), default=0)
        widths = {"Format": max(6, fmt_max)}
        for alg in algs:
            widths[alg] = len(labels[alg])
        for fmt in fmts:
            for alg in algs:
                vals = data.get((fmt,alg), [])
                txt = f"{statistics.mean(vals):.1f} σ {statistics.pstdev(vals):.1f}" if vals else "n.a"
                widths[alg] = max(widths[alg], len(txt))

        # header
        left  = "Format".ljust(widths["Format"])
        freeW = widths["erepair"] + 3 + widths["DDMax"]
        depW  = widths["DDMaxG"]  + 3 + widths["Antlr"]
        print(f"| {left} | {'Format-free'.center(freeW)} | {'Format-dependent'.center(depW)} |")
        print("| " + " "*widths["Format"] +
              " | " + labels["erepair"].ljust(widths["erepair"]) +
              " | " + labels["DDMax"].ljust(widths["DDMax"]) +
              " | " + labels["DDMaxG"].ljust(widths["DDMaxG"]) +
              " | " + labels["Antlr"].ljust(widths["Antlr"]) + " |")
        print("|-" + "-|-".join("-"*widths[c] for c in (["Format"]+algs)) + "-|")

        # rows
        for fmt in fmts:
            row = [fmt.upper().ljust(widths["Format"])]
            for alg in algs:
                vals = data.get((fmt,alg), [])
                cell = f"{statistics.mean(vals):.1f} σ {statistics.pstdev(vals):.1f}" if vals else "n.a"
                row.append(cell.ljust(widths[alg]))
            print("| " + " | ".join(row) + " |")

    # bottom summary
    sep = "|-" + "-|-".join("-"*widths[c] for c in (["Format"]+algs)) + "-|"
    print(sep)
    avg_row = ["Average"] + [
        (f"{statistics.mean(agg_vals[alg]):.1f} σ {statistics.pstdev(agg_vals[alg]):.1f}"
         if agg_vals[alg] else "n.a")
        for alg in algs
    ]
    rec_row = ["Recovery"] + [
        (f"{statistics.mean(agg_flags[alg])*100:.0f}% σ {statistics.pstdev(agg_flags[alg])*100:.2f}"
         if agg_flags[alg] else "n.a")
        for alg in algs
    ]
    print("| " +
          avg_row[0].ljust(widths["Format"]) + " | " +
          " | ".join(avg_row[i].ljust(widths[algs[i-1]]) for i in range(1,len(algs)+1)) +
          " |")
    print("| " +
          rec_row[0].ljust(widths["Format"]) + " | " +
          " | ".join(rec_row[i].ljust(widths[algs[i-1]]) for i in range(1,len(algs)+1)) +
          " |")

def print_table_v(single_db: str, double_db: str, trunc_db: str):
    # TABLE V: distance_original_repaired mean±σ for fixed=1, plus avg & recovery
    scenarios = [("Single", single_db), ("Double", double_db), ("Truncated", trunc_db)]
    algs   = ["erepair","DDMax","DDMaxG","Antlr"]
    labels = {"erepair":"εREPAIR","DDMax":"DDMax","DDMaxG":"DDMaxG","Antlr":"ANTLR"}

    print("\n**TABLE V: Distance from original data to repaired data**\n")
    agg_vals = {alg:[] for alg in algs}
    agg_flags= {alg:[] for alg in algs}

    for name, db in scenarios:
        conn = sqlite3.connect(db); cur = conn.cursor()
        cur.execute("""
            SELECT format, algorithm, distance_original_repaired, fixed
              FROM results
        """)
        data: Dict[Tuple[str,str], List[int]] = {}
        for fmt, alg, dist, fixed in cur.fetchall():
            di = safe_int(dist)
            fi = safe_int(fixed)
            if fi is not None:
                agg_flags[alg].append(fi)
            if di is not None and fi == 1:
                data.setdefault((str(fmt), alg), []).append(di)
                agg_vals[alg].append(di)
        conn.close()

        fmts = sorted({fmt for fmt,_ in data})
        if not fmts:
            continue

        fmt_max = max((len(f) for f in fmts), default=0)
        widths  = {"Format": max(6, fmt_max)}
        for alg in algs:
            widths[alg] = len(labels[alg])
        for fmt in fmts:
            for alg in algs:
                vals = data.get((fmt,alg), [])
                txt = f"{statistics.mean(vals):.1f} σ {statistics.pstdev(vals):.1f}" if vals else "n.a"
                widths[alg] = max(widths[alg], len(txt))

        left, freeW, depW = (
            "Format".ljust(widths["Format"]),
            widths["erepair"]+3+widths["DDMax"],
            widths["DDMaxG"] +3+widths["Antlr"]
        )
        print(f"| {left} | {'Format-free'.center(freeW)} | {'Format-dependent'.center(depW)} |")
        print("| " + " "*widths["Format"] +
              " | " + labels["erepair"].ljust(widths["erepair"]) +
              " | " + labels["DDMax"].ljust(widths["DDMax"]) +
              " | " + labels["DDMaxG"].ljust(widths["DDMaxG"]) +
              " | " + labels["Antlr"].ljust(widths["Antlr"]) + " |")
        print("|-"+ "-|-".join("-"*widths[c] for c in (["Format"]+algs)) + "-|")

        for fmt in fmts:
            row = [fmt.upper().ljust(widths["Format"])]
            for alg in algs:
                vals = data.get((fmt,alg), [])
                cell = f"{statistics.mean(vals):.1f} σ {statistics.pstdev(vals):.1f}" if vals else "n.a"
                row.append(cell.ljust(widths[alg]))
            print("| " + " | ".join(row) + " |")

    sep = "|-"+ "-|-".join("-"*widths[c] for c in (["Format"]+algs)) + "-|"
    print(sep)
    avg_row = ["Average"] + [
        (f"{statistics.mean(agg_vals[alg]):.1f} σ {statistics.pstdev(agg_vals[alg]):.1f}"
         if agg_vals[alg] else "n.a")
        for alg in algs
    ]
    rec_row = ["Recovery"] + [
        (f"{statistics.mean(agg_flags[alg])*100:.0f}% σ {statistics.pstdev(agg_flags[alg])*100:.2f}"
         if agg_flags[alg] else "n.a")
        for alg in algs
    ]
    print("| " +
          avg_row[0].ljust(widths["Format"]) + " | " +
          " | ".join(avg_row[i].ljust(widths[algs[i-1]]) for i in range(1,len(algs)+1)) +
          " |")
    print("| " +
          rec_row[0].ljust(widths["Format"]) + " | " +
          " | ".join(rec_row[i].ljust(widths[algs[i-1]]) for i in range(1,len(algs)+1)) +
          " |")

def print_table_vi(single_db, double_db, trunc_db):
    # TABLE VI: count of fixed=1 per (scenario,format,alg) + Total
    scenarios = [("Single", single_db), ("Double", double_db), ("Truncated", trunc_db)]
    algs = ["erepair","DDMax","DDMaxG","Antlr"]

    acc = defaultdict(int)
    for name, db in scenarios:
        c = sqlite3.connect(db).cursor()
        c.execute("SELECT format, algorithm, fixed FROM results")
        for fmt, alg, fixed in c.fetchall():
            fi = safe_int(fixed)
            if fi == 1:
                acc[(name, str(fmt).upper(), alg)] += 1
        c.connection.close()

    rows = []
    for name, _ in scenarios:
        fmts = sorted({fmt for (n,fmt,_) in acc if n == name})
        for fmt in fmts:
            row = [name, fmt] + [ str(acc.get((name, fmt, alg),0)) for alg in algs ]
            rows.append(row)
    total = ["Total",""] + [ str(sum(int(r[2+i]) for r in rows)) for i in range(len(algs)) ]
    rows.append(total)

    hdr = ["Scenario","Format"] + algs
    widths = {h:len(h) for h in hdr}
    for r in rows:
        for i,c in enumerate(r):
            widths[hdr[i]] = max(widths[hdr[i]], len(c))

    print("\n**TABLE VI: Number of corrupt records repaired**\n")
    print("| " + " | ".join(h.ljust(widths[h]) for h in hdr) + " |")
    print("|-" + "-|-".join("-"*widths[h] for h in hdr) + "-|")
    for r in rows:
        print("| " + " | ".join(r[i].ljust(widths[hdr[i]]) for i in range(len(hdr))) + " |")

def print_table_vii(single_db, double_db, trunc_db):
    # TABLE VII: perfectly repaired (fixed=1 & distance_original_repaired=0)
    scenarios = [("Single", single_db), ("Double", double_db), ("Truncated", trunc_db)]
    algs = ["erepair","DDMax","DDMaxG","Antlr"]

    acc = defaultdict(int)
    for name, db in scenarios:
        c = sqlite3.connect(db).cursor()
        c.execute("SELECT format, algorithm, fixed, distance_original_repaired FROM results")
        for fmt, alg, fixed, dor in c.fetchall():
            fi = safe_int(fixed); di = safe_int(dor)
            if fi == 1 and di == 0:
                acc[(name, str(fmt).upper(), alg)] += 1
        c.connection.close()

    rows = []
    for name, _ in scenarios:
        fmts = sorted({fmt for (n,fmt,_) in acc if n == name})
        for fmt in fmts:
            row = [name, fmt] + [ str(acc.get((name, fmt, alg),0)) for alg in algs]
            rows.append(row)

    hdr = ["Scenario","Format"] + algs
    widths = {h:len(h) for h in hdr}
    for r in rows:
        for i,c in enumerate(r):
            widths[hdr[i]] = max(widths[hdr[i]], len(c))

    print("\n**TABLE VII: Number of perfectly repaired files**\n")
    print("| " + " | ".join(h.ljust(widths[h]) for h in hdr) + " |")
    print("|-" + "-|-".join("-"*widths[h] for h in hdr) + "-|")
    for r in rows:
        print("| " + " | ".join(r[i].ljust(widths[hdr[i]]) for i in range(len(hdr))) + " |")

def print_table_viii(single_db, double_db, trunc_db):
    # TABLE VIII: avg repair_time & sum iterations for fixed=1
    dbs = [single_db,double_db,trunc_db]
    algs = ["erepair","DDMax","DDMaxG","Antlr"]

    times = defaultdict(list)
    iters = defaultdict(int)

    for db in dbs:
        c = sqlite3.connect(db).cursor()
        c.execute("SELECT algorithm, fixed, iterations, repair_time FROM results")
        for alg, fixed, it, rt in c.fetchall():
            fi = safe_int(fixed)
            if fi == 1:
                iters[alg] += safe_int(it) or 0
                try:
                    times[alg].append(float(rt))
                except:
                    pass
        c.connection.close()

    hdr = ["Metric"] + algs
    widths = {h:len(h) for h in hdr}

    rt_row = ["Runtime"] + [
        (f"{statistics.mean(times[alg]):.2f} secs" if times[alg] else "n.a")
        for alg in algs
    ]
    ex_row = ["#Execs"] + [
        (str(iters[alg]) if iters[alg] else "n.a")
        for alg in algs
    ]
    for i,alg in enumerate(algs,1):
        widths[alg] = max(widths[alg], len(rt_row[i]), len(ex_row[i]))

    print("\n**TABLE VIII: Efficiency of data repair (Average)**\n")
    print("| " + " | ".join(h.ljust(widths[h]) for h in hdr) + " |")
    print("|-" + "-|-".join("-"*widths[h] for h in hdr) + "-|")
    print("| " + " | ".join(rt_row[i].ljust(widths[hdr[i]]) for i in range(len(hdr))) + " |")
    print("| " + " | ".join(ex_row[i].ljust(widths[hdr[i]]) for i in range(len(hdr))) + " |")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--single",    required=True)
    p.add_argument("--double",    required=True)
    p.add_argument("--truncated", required=True)
    args = p.parse_args()

    print_table_iii(args.single, args.double, args.truncated)
    print_table_iv(args.single, args.double, args.truncated)
    print_table_v(args.single, args.double, args.truncated)
    print_table_vi(args.single, args.double, args.truncated)
    print_table_vii(args.single, args.double, args.truncated)
    print_table_viii(args.single, args.double, args.truncated)

if __name__ == "__main__":
    main()