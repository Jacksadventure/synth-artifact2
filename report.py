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

Now supports filtering by multiple formats via `--format` (case-insensitive).
"""

import argparse
import sqlite3
import statistics
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


def safe_int(x):
    try:
        return int(x)
    except:
        return None


def print_table_iii(single_db: str, double_db: str, trunc_db: str, fmt_filter: Optional[List[str]] = None):
    # TABLE III: counts & record-length mean±σ in single_db
    def load_counts(db: str) -> Dict[str, int]:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT format, COUNT(*) FROM results GROUP BY format")
        d = {fmt: cnt for fmt, cnt in cur.fetchall()}
        conn.close()
        return d

    def load_lengths(db: str) -> Dict[str, List[int]]:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT format, LENGTH(original_text) FROM results")
        d: Dict[str, List[int]] = {}
        for fmt, L in cur.fetchall():
            d.setdefault(fmt, []).append(L)
        conn.close()
        return d

    sc = load_counts(single_db)
    dc = load_counts(double_db)
    tc = load_counts(trunc_db)
    lengths = load_lengths(single_db)
    fmts = sorted(set(sc) | set(dc) | set(tc))
    
    if fmt_filter:
        fmt_filter_lower = [f.lower() for f in fmt_filter]
        fmts = [f for f in fmts if f.lower() in fmt_filter_lower]

    hdr = ["Format", "Record Len.", "Single Corr.", "Double Corr.", "Truncated"]
    widths = {h: len(h) for h in hdr}
    rows = []
    for f in fmts:
        lens = lengths.get(f, [])
        if lens:
            m = statistics.mean(lens)
            s = statistics.pstdev(lens) if len(lens) > 1 else 0.0
            rec = f"{m:.1f} σ {s:.1f}"
        else:
            rec = "N/A"
        sct, dct, tct = sc.get(f, 0), dc.get(f, 0), tc.get(f, 0)
        pct = (tct * 100 / sct) if sct else 0.0
        tr = f"{tct} ({pct:.1f}%)"
        row = [f.upper(), rec, str(sct), str(dct), tr]
        rows.append(row)
        for h, cell in zip(hdr, row):
            widths[h] = max(widths[h], len(cell))

    print("\n**TABLE III: Number of corrupt inputs**\n")
    print("| " + " | ".join(h.ljust(widths[h]) for h in hdr) + " |")
    print("|-" + "-|-".join("-" * widths[h] for h in hdr) + "-|")
    for r in rows:
        print("| " + " | ".join(r[i].ljust(widths[hdr[i]]) for i in range(len(hdr))) + " |")


def print_table_iv(single_db: str, double_db: str, trunc_db: str, fmt_filter: Optional[List[str]] = None):
    # TABLE IV: distance_broken_repaired for fixed=1
    scenarios = [("Single", single_db), ("Double", double_db), ("Truncated", trunc_db)]
    algs = ["erepair", "DDMax", "DDMaxG", "Antlr"]
    labels = {"erepair": "εREPAIR", "DDMax": "DDMax", "DDMaxG": "DDMaxG", "Antlr": "ANTLR"}

    print("\n**TABLE IV: Distance between corrupt data and repaired data**\n")
    
    fmt_filter_lower = [f.lower() for f in fmt_filter] if fmt_filter else None
    
    agg_vals = {alg: [] for alg in algs}
    agg_flags = {alg: [] for alg in algs}

    # Widths for the summary section, initialized and updated to be max across all scenarios and summary content
    summary_section_widths = {"Format": max(len("Format"), len("Average"), len("Recovery"))}
    for alg in algs:
        summary_section_widths[alg] = len(labels[alg])
    
    any_scenario_printed = False

    for name, db in scenarios:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT format, algorithm, distance_broken_repaired, fixed FROM results")
        data: Dict[Tuple[str, str], List[int]] = {}
        for fmt_sql, alg_sql, dist_sql, fixed_sql in cur.fetchall():
            if fmt_filter_lower and fmt_sql.lower() not in fmt_filter_lower:
                continue
            di = safe_int(dist_sql)
            fi = safe_int(fixed_sql)
            if fi is not None: # Fixed status (0 or 1)
                agg_flags[alg_sql].append(fi)
            if di is not None and fi == 1: # Distance for successfully repaired
                data.setdefault((fmt_sql, alg_sql), []).append(di)
                agg_vals[alg_sql].append(di)
        conn.close()

        fmts_this_scenario = sorted({fmt for fmt, _ in data})
        if not fmts_this_scenario:
            continue # Skip printing this scenario's table part if no relevant data
        
        any_scenario_printed = True

        # Calculate widths for THIS scenario's section
        current_scenario_widths = {"Format": max(6, max((len(f) for f in fmts_this_scenario), default=0))}
        for alg in algs:
            current_scenario_widths[alg] = len(labels[alg])
        
        for fmt_row_hdr in fmts_this_scenario:
            for alg_col_hdr in algs:
                vals = data.get((fmt_row_hdr, alg_col_hdr), [])
                txt = (f"{statistics.mean(vals):.1f} σ {statistics.pstdev(vals):.1f}" if len(vals) > 1 
                       else f"{statistics.mean(vals):.1f} σ 0.0" if len(vals) == 1 else "n.a")
                current_scenario_widths[alg_col_hdr] = max(current_scenario_widths[alg_col_hdr], len(txt))

        # Print this scenario's section header and data
        left_label = "Format".ljust(current_scenario_widths["Format"])
        free_width_val = current_scenario_widths["erepair"] + 3 + current_scenario_widths["DDMax"]
        dep_width_val = current_scenario_widths["DDMaxG"] + 3 + current_scenario_widths["Antlr"]
        print(f"Scenario: {name}") # Indicate which scenario this block is for
        print(f"| {left_label} | {'Format-free'.center(free_width_val)} | {'Format-dependent'.center(dep_width_val)} |")
        
        header_parts = [" " * current_scenario_widths["Format"]]
        for alg in algs:
            header_parts.append(labels[alg].ljust(current_scenario_widths[alg]))
        print("| " + " | ".join(header_parts) + " |")
        
        cols_for_sep = ["Format"] + algs
        print("|-" + "-|-".join("-" * current_scenario_widths[c] for c in cols_for_sep) + "-|")

        for fmt_row_hdr in fmts_this_scenario:
            row_output = [fmt_row_hdr.upper().ljust(current_scenario_widths["Format"])]
            for alg_col_hdr in algs:
                vals = data.get((fmt_row_hdr, alg_col_hdr), [])
                cell = (f"{statistics.mean(vals):.1f} σ {statistics.pstdev(vals):.1f}" if len(vals) > 1
                        else f"{statistics.mean(vals):.1f} σ 0.0" if len(vals) == 1 else "n.a")
                row_output.append(cell.ljust(current_scenario_widths[alg_col_hdr]))
            print("| " + " | ".join(row_output) + " |")
        print() # Add a blank line after each scenario's table part

        # Update summary_section_widths to be max of itself and current_scenario_widths
        for col_key in current_scenario_widths:
             summary_section_widths[col_key] = max(summary_section_widths.get(col_key,0) , current_scenario_widths[col_key])

    if not any_scenario_printed and not (agg_vals or agg_flags): # if no data was processed at all
        print("No data to display for the selected filters.")
        return

    # Summary rows (aggregated across formats and scenarios)
    avg_row_text_cells = ["Average"]
    for alg in algs:
        text = (f"{statistics.mean(agg_vals[alg]):.1f} σ {statistics.pstdev(agg_vals[alg]):.1f}" if len(agg_vals[alg]) > 1
                else f"{statistics.mean(agg_vals[alg]):.1f} σ 0.0" if len(agg_vals[alg]) == 1 else "n.a")
        avg_row_text_cells.append(text)
        summary_section_widths[alg] = max(summary_section_widths[alg], len(text))

    rec_row_text_cells = ["Recovery"]
    for alg in algs:
        text = (f"{statistics.mean(agg_flags[alg]) * 100:.0f}% σ {statistics.pstdev(agg_flags[alg]) * 100:.2f}" if len(agg_flags[alg]) > 1
                else f"{statistics.mean(agg_flags[alg]) * 100:.0f}% σ 0.00" if len(agg_flags[alg]) == 1 else "n.a") # pstdev of single value is 0
        rec_row_text_cells.append(text)
        summary_section_widths[alg] = max(summary_section_widths[alg], len(text))
    
    summary_section_widths["Format"] = max(summary_section_widths["Format"], len("Average"), len("Recovery"))


    print("Summary (across all applicable scenarios and formats):")
    sep = "|-" + "-|-".join("-" * summary_section_widths[c] for c in (["Format"] + algs)) + "-|"
    print(sep)
    
    avg_print_row = [avg_row_text_cells[0].ljust(summary_section_widths["Format"])]
    for i, alg_hdr in enumerate(algs):
        avg_print_row.append(avg_row_text_cells[i+1].ljust(summary_section_widths[alg_hdr]))
    print("| " + " | ".join(avg_print_row) + " |")

    rec_print_row = [rec_row_text_cells[0].ljust(summary_section_widths["Format"])]
    for i, alg_hdr in enumerate(algs):
        rec_print_row.append(rec_row_text_cells[i+1].ljust(summary_section_widths[alg_hdr]))
    print("| " + " | ".join(rec_print_row) + " |")


def print_table_v(single_db: str, double_db: str, trunc_db: str, fmt_filter: Optional[List[str]] = None):
    # TABLE V: distance_original_repaired for fixed=1
    # This function is structurally identical to print_table_iv, only differing in the SQL query column
    # and the table title. We use the same logic for multi-format filtering and width handling.
    
    scenarios = [("Single", single_db), ("Double", double_db), ("Truncated", trunc_db)]
    algs = ["erepair", "DDMax", "DDMaxG", "Antlr"]
    labels = {"erepair": "εREPAIR", "DDMax": "DDMax", "DDMaxG": "DDMaxG", "Antlr": "ANTLR"}

    print("\n**TABLE V: Distance from original data to repaired data**\n")
    
    fmt_filter_lower = [f.lower() for f in fmt_filter] if fmt_filter else None
    
    agg_vals = {alg: [] for alg in algs}
    agg_flags = {alg: [] for alg in algs} # For recovery rate, same as Table IV

    summary_section_widths = {"Format": max(len("Format"), len("Average"), len("Recovery"))}
    for alg in algs:
        summary_section_widths[alg] = len(labels[alg])

    any_scenario_printed = False

    for name, db in scenarios:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        # Key difference: distance_original_repaired
        cur.execute("SELECT format, algorithm, distance_original_repaired, fixed FROM results")
        data: Dict[Tuple[str, str], List[int]] = {}
        for fmt_sql, alg_sql, dist_sql, fixed_sql in cur.fetchall():
            if fmt_filter_lower and fmt_sql.lower() not in fmt_filter_lower:
                continue
            di = safe_int(dist_sql)
            fi = safe_int(fixed_sql)
            if fi is not None:
                agg_flags[alg_sql].append(fi)
            if di is not None and fi == 1:
                data.setdefault((fmt_sql, alg_sql), []).append(di)
                agg_vals[alg_sql].append(di)
        conn.close()

        fmts_this_scenario = sorted({fmt for fmt, _ in data})
        if not fmts_this_scenario:
            continue
        
        any_scenario_printed = True

        current_scenario_widths = {"Format": max(6, max((len(f) for f in fmts_this_scenario), default=0))}
        for alg in algs:
            current_scenario_widths[alg] = len(labels[alg])
        
        for fmt_row_hdr in fmts_this_scenario:
            for alg_col_hdr in algs:
                vals = data.get((fmt_row_hdr, alg_col_hdr), [])
                txt = (f"{statistics.mean(vals):.1f} σ {statistics.pstdev(vals):.1f}" if len(vals) > 1 
                       else f"{statistics.mean(vals):.1f} σ 0.0" if len(vals) == 1 else "n.a")
                current_scenario_widths[alg_col_hdr] = max(current_scenario_widths[alg_col_hdr], len(txt))
        
        left_label = "Format".ljust(current_scenario_widths["Format"])
        free_width_val = current_scenario_widths["erepair"] + 3 + current_scenario_widths["DDMax"]
        dep_width_val = current_scenario_widths["DDMaxG"] + 3 + current_scenario_widths["Antlr"]
        print(f"Scenario: {name}")
        print(f"| {left_label} | {'Format-free'.center(free_width_val)} | {'Format-dependent'.center(dep_width_val)} |")
        
        header_parts = [" " * current_scenario_widths["Format"]]
        for alg in algs:
            header_parts.append(labels[alg].ljust(current_scenario_widths[alg]))
        print("| " + " | ".join(header_parts) + " |")
        
        cols_for_sep = ["Format"] + algs
        print("|-" + "-|-".join("-" * current_scenario_widths[c] for c in cols_for_sep) + "-|")

        for fmt_row_hdr in fmts_this_scenario:
            row_output = [fmt_row_hdr.upper().ljust(current_scenario_widths["Format"])]
            for alg_col_hdr in algs:
                vals = data.get((fmt_row_hdr, alg_col_hdr), [])
                cell = (f"{statistics.mean(vals):.1f} σ {statistics.pstdev(vals):.1f}" if len(vals) > 1
                        else f"{statistics.mean(vals):.1f} σ 0.0" if len(vals) == 1 else "n.a")
                row_output.append(cell.ljust(current_scenario_widths[alg_col_hdr]))
            print("| " + " | ".join(row_output) + " |")
        print()

        for col_key in current_scenario_widths:
             summary_section_widths[col_key] = max(summary_section_widths.get(col_key,0) , current_scenario_widths[col_key])
    
    if not any_scenario_printed and not (agg_vals or agg_flags):
        print("No data to display for the selected filters.")
        return

    avg_row_text_cells = ["Average"]
    for alg in algs:
        text = (f"{statistics.mean(agg_vals[alg]):.1f} σ {statistics.pstdev(agg_vals[alg]):.1f}" if len(agg_vals[alg]) > 1
                else f"{statistics.mean(agg_vals[alg]):.1f} σ 0.0" if len(agg_vals[alg]) == 1 else "n.a")
        avg_row_text_cells.append(text)
        summary_section_widths[alg] = max(summary_section_widths[alg], len(text))

    rec_row_text_cells = ["Recovery"] # Same recovery rate as Table IV
    for alg in algs:
        text = (f"{statistics.mean(agg_flags[alg]) * 100:.0f}% σ {statistics.pstdev(agg_flags[alg]) * 100:.2f}" if len(agg_flags[alg]) > 1
                else f"{statistics.mean(agg_flags[alg]) * 100:.0f}% σ 0.00" if len(agg_flags[alg]) == 1 else "n.a")
        rec_row_text_cells.append(text)
        summary_section_widths[alg] = max(summary_section_widths[alg], len(text))
        
    summary_section_widths["Format"] = max(summary_section_widths["Format"], len("Average"), len("Recovery"))

    print("Summary (across all applicable scenarios and formats):")
    sep = "|-" + "-|-".join("-" * summary_section_widths[c] for c in (["Format"] + algs)) + "-|"
    print(sep)

    avg_print_row = [avg_row_text_cells[0].ljust(summary_section_widths["Format"])]
    for i, alg_hdr in enumerate(algs):
        avg_print_row.append(avg_row_text_cells[i+1].ljust(summary_section_widths[alg_hdr]))
    print("| " + " | ".join(avg_print_row) + " |")

    rec_print_row = [rec_row_text_cells[0].ljust(summary_section_widths["Format"])]
    for i, alg_hdr in enumerate(algs):
        rec_print_row.append(rec_row_text_cells[i+1].ljust(summary_section_widths[alg_hdr]))
    print("| " + " | ".join(rec_print_row) + " |")


def print_table_vi(single_db: str, double_db: str, trunc_db: str, fmt_filter: Optional[List[str]] = None):
    # TABLE VI: count of fixed=1 per (scenario, format, alg)
    scenarios = [("Single", single_db), ("Double", double_db), ("Truncated", trunc_db)]
    algs = ["erepair", "DDMax", "DDMaxG", "Antlr"]

    fmt_filter_lower = [f.lower() for f in fmt_filter] if fmt_filter else None

    acc = defaultdict(int)
    for name, db in scenarios:
        conn = sqlite3.connect(db); cur = conn.cursor()
        cur.execute("SELECT format, algorithm, fixed FROM results")
        for fmt_sql, alg_sql, fixed_sql in cur.fetchall():
            if fmt_filter_lower and fmt_sql.lower() not in fmt_filter_lower:
                continue
            fi = safe_int(fixed_sql)
            if fi == 1:
                acc[(name, fmt_sql.upper(), alg_sql)] += 1
        conn.close()

    rows = []
    processed_fmts_overall = set()
    for name, _ in scenarios:
        fmts_this_scenario = sorted({fmt for (n, fmt, _) in acc if n == name})
        for fmt_row_hdr in fmts_this_scenario:
            processed_fmts_overall.add(fmt_row_hdr)
            row = [name, fmt_row_hdr] + [str(acc.get((name, fmt_row_hdr, alg_col_hdr), 0)) for alg_col_hdr in algs]
            rows.append(row)
    
    if not rows and fmt_filter: # If filtering resulted in no data
        print("\n**TABLE VI: Number of corrupt records repaired**\n")
        print("No data to display for the selected filters.")
        return
        
    total_row_data = [0] * len(algs)
    for r_data in rows:
        for i in range(len(algs)):
            total_row_data[i] += int(r_data[2+i])
    
    total = ["Total", ""] + [str(s) for s in total_row_data]
    rows.append(total)


    hdr = ["Scenario", "Format"] + algs
    widths = {h: len(h) for h in hdr}
    for r_data in rows:
        for i, cell in enumerate(r_data):
            widths[hdr[i]] = max(widths[hdr[i]], len(cell))

    print("\n**TABLE VI: Number of corrupt records repaired**\n")
    print("| " + " | ".join(h.ljust(widths[h]) for h in hdr) + " |")
    print("|-" + "-|-".join("-" * widths[h] for h in hdr) + "-|")
    for r_data in rows:
        print("| " + " | ".join(r_data[i].ljust(widths[hdr[i]]) for i in range(len(hdr))) + " |")


def print_table_vii(single_db: str, double_db: str, trunc_db: str, fmt_filter: Optional[List[str]] = None):
    # TABLE VII: perfectly repaired (fixed=1 & distance_original_repaired=0)
    scenarios = [("Single", single_db), ("Double", double_db), ("Truncated", trunc_db)]
    algs = ["erepair", "DDMax", "DDMaxG", "Antlr"]

    fmt_filter_lower = [f.lower() for f in fmt_filter] if fmt_filter else None

    acc = defaultdict(int)
    for name, db in scenarios:
        conn = sqlite3.connect(db); cur = conn.cursor()
        cur.execute("SELECT format, algorithm, fixed, distance_original_repaired FROM results")
        for fmt_sql, alg_sql, fixed_sql, dor_sql in cur.fetchall():
            if fmt_filter_lower and fmt_sql.lower() not in fmt_filter_lower:
                continue
            fi = safe_int(fixed_sql); di = safe_int(dor_sql)
            if fi == 1 and di == 0:
                acc[(name, fmt_sql.upper(), alg_sql)] += 1
        conn.close()

    rows = []
    processed_fmts_overall = set() # Track if any format data is processed
    for name, _ in scenarios:
        fmts_this_scenario = sorted({fmt for (n, fmt, _) in acc if n == name})
        for fmt_row_hdr in fmts_this_scenario:
            processed_fmts_overall.add(fmt_row_hdr)
            row = [name, fmt_row_hdr] + [str(acc.get((name, fmt_row_hdr, alg_col_hdr), 0)) for alg_col_hdr in algs]
            rows.append(row)

    if not rows and fmt_filter: # If filtering resulted in no data
        print("\n**TABLE VII: Number of perfectly repaired files**\n")
        print("No data to display for the selected filters.")
        return

    # Adding a total row, similar to Table VI, though not in original script for VII.
    # This can be useful. If not desired, this block can be removed.
    total_row_data = [0] * len(algs)
    for r_data in rows: # Calculate totals if rows exist
        for i in range(len(algs)):
            total_row_data[i] += int(r_data[2+i]) # Sum counts for each algorithm
    
    if rows: # Only add total row if there's data
        total = ["Total", ""] + [str(s) for s in total_row_data]
        rows.append(total)


    hdr = ["Scenario", "Format"] + algs
    widths = {h: len(h) for h in hdr}
    for r_data in rows: # Calculate widths based on all rows including total
        for i, cell in enumerate(r_data):
            widths[hdr[i]] = max(widths[hdr[i]], len(cell))

    print("\n**TABLE VII: Number of perfectly repaired files**\n")
    print("| " + " | ".join(h.ljust(widths[h]) for h in hdr) + " |")
    print("|-" + "-|-".join("-" * widths[h] for h in hdr) + "-|")
    for r_data in rows:
        print("| " + " | ".join(r_data[i].ljust(widths[hdr[i]]) for i in range(len(hdr))) + " |")


def print_table_viii(single_db: str, double_db: str, trunc_db: str, fmt_filter: Optional[List[str]] = None):
    # TABLE VIII: avg repair_time & sum iterations for fixed=1
    dbs = [single_db, double_db, trunc_db]
    algs = ["erepair", "DDMax", "DDMaxG", "Antlr"]

    fmt_filter_lower = [f.lower() for f in fmt_filter] if fmt_filter else None

    times = defaultdict(list)
    iters = defaultdict(int)
    
    data_found = False

    for db in dbs:
        conn = sqlite3.connect(db); cur = conn.cursor()
        cur.execute("SELECT format, algorithm, fixed, iterations, repair_time FROM results")
        for fmt_sql, alg_sql, fixed_sql, it_sql, rt_sql in cur.fetchall():
            if fmt_filter_lower and fmt_sql.lower() not in fmt_filter_lower:
                continue
            
            data_found = True # Mark that we've processed at least one row matching filters
            
            fi = safe_int(fixed_sql)
            if fi == 1:
                iters[alg_sql] += safe_int(it_sql) or 0
                try:
                    times[alg_sql].append(float(rt_sql))
                except (TypeError, ValueError): # Handles None or non-float rt_sql
                    pass
        conn.close()

    if not data_found and fmt_filter:
        print("\n**TABLE VIII: Efficiency of data repair (Average)**\n")
        print("No data to display for the selected filters.")
        return

    hdr = ["Metric"] + algs
    widths = {h: len(h) for h in hdr}

    rt_row_cells = ["Runtime"]
    for alg in algs:
        cell = (f"{statistics.mean(times[alg]):.2f} secs" if times[alg] else "n.a")
        rt_row_cells.append(cell)

    ex_row_cells = ["#Execs"]
    for alg in algs:
        cell = (str(iters[alg]) if iters[alg] or alg in times and times[alg] else "n.a") # show 0 if fixed=1 items existed but iters sum to 0
        ex_row_cells.append(cell)

    for i, alg_hdr in enumerate(algs, 1):
        widths[alg_hdr] = max(widths[alg_hdr], len(rt_row_cells[i]), len(ex_row_cells[i]))
    widths["Metric"] = max(widths["Metric"], len(rt_row_cells[0]), len(ex_row_cells[0]))


    print("\n**TABLE VIII: Efficiency of data repair (Average)**\n")
    print("| " + " | ".join(h.ljust(widths[h]) for h in hdr) + " |")
    print("|-" + "-|-".join("-" * widths[h] for h in hdr) + "-|")
    
    rt_print_row = [rt_row_cells[0].ljust(widths["Metric"])] + \
                   [rt_row_cells[i].ljust(widths[algs[i-1]]) for i in range(1, len(algs)+1)]
    print("| " + " | ".join(rt_print_row) + " |")

    ex_print_row = [ex_row_cells[0].ljust(widths["Metric"])] + \
                   [ex_row_cells[i].ljust(widths[algs[i-1]]) for i in range(1, len(algs)+1)]
    print("| " + " | ".join(ex_print_row) + " |")


def main():
    p = argparse.ArgumentParser(description="Generate TABLES III–VIII from SQLite DBs.")
    p.add_argument("--single", required=True, help="Path to single-byte corruptions SQLite DB")
    p.add_argument("--double", required=True, help="Path to double-byte corruptions SQLite DB")
    p.add_argument("--truncated", required=True, help="Path to truncated inputs SQLite DB")
    p.add_argument("--format", dest="fmt", nargs='+', help="Filter results by one or more formats (case-insensitive). E.g., --format CSV JSON")
    args = p.parse_args()

    # Handle pstdev for single-element lists more gracefully (returns 0)
    # The code within table functions now checks len(list) > 1 for pstdev.
    # For mean, len(list) >= 1 is sufficient. statistics.mean([]) raises error.

    print_table_iii(args.single, args.double, args.truncated, args.fmt)
    print_table_iv(args.single, args.double, args.truncated, args.fmt)
    print_table_v(args.single, args.double, args.truncated, args.fmt)
    print_table_vi(args.single, args.double, args.truncated, args.fmt)
    print_table_vii(args.single, args.double, args.truncated, args.fmt)
    print_table_viii(args.single, args.double, args.truncated, args.fmt)

if __name__ == "__main__":
    main()