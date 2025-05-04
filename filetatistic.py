#!/usr/bin/env python3
"""
mine_counts.py – count #Crawled / #Unique / MeanSizeKiB per input format
-------------------------------------------------------------------------
示例目录：
original_files/
├── ini_data/   ─ file1.ini …
├── json_data/  ─ a.json …
└── lisp_data/  ─ …

运行示例：
    python mine_counts.py                       # 默认 ./original_files
    python mine_counts.py -p ../data -o table.csv
"""
import argparse
from pathlib import Path
import csv
from collections import defaultdict

def kib(bytes_):
    """Bytes → KiB（取两位小数）"""
    return round(bytes_ / 1024, 2)

def collect_counts(root: Path):
    stats = defaultdict(lambda: {"crawled": 0,
                                 "unique": set(),
                                 "size_sum": 0})

    for sub in root.iterdir():
        if not sub.is_dir():
            continue
        fmt = sub.name.replace("_data", "").upper()          # json_data → JSON
        for f in sub.rglob("*"):
            if f.is_file():
                stats[fmt]["crawled"] += 1
                stats[fmt]["unique"].add(f.name)
                stats[fmt]["size_sum"] += f.stat().st_size    # 累加字节数

    rows = []
    for fmt, s in stats.items():
        mean_kib = kib(s["size_sum"] / s["crawled"]) if s["crawled"] else 0
        rows.append({
            "Input Format": fmt,
            "#Crawled Files": s["crawled"],
            "#Unique Files": len(s["unique"]),
            "Mean Size (KiB)": mean_kib
        })
    return sorted(rows, key=lambda r: r["Input Format"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", default="original_files",
                    help="Directory containing *_data subfolders (default: %(default)s)")
    ap.add_argument("-o", "--out", default="mined_input_files.csv",
                    help="CSV output path (default: %(default)s)")
    args = ap.parse_args()

    root = Path(args.path).expanduser()
    if not root.is_dir():
        ap.error(f"{root} is not a directory")

    rows = collect_counts(root)

    header = ["Input Format", "#Crawled Files", "#Unique Files", "Mean Size (KiB)"]
    print("\t".join(header))
    for r in rows:
        print("\t".join(map(str, [r[h] for h in header])))

    with open(args.out, "w", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWritten → {args.out}")

if __name__ == "__main__":
    main()