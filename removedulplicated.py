#!/usr/bin/env python3
"""
dedup_results.py  –  Drop duplicates in result1.db

Unique key = (algorithm, original_text)
Keeps the smallest id in each group, deletes the rest.
"""

import sqlite3, os

RESULT_DB = "result1.db"

def dedup_results(db_path: str):
    if not os.path.exists(db_path):
        raise SystemExit(f"{db_path} not found")

    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()

    # ① 找出要保留的最小 id
    cur.execute("""
        SELECT MIN(id) AS keep_id
        FROM results
        GROUP BY algorithm, original_text
    """)
    keep_ids = {row[0] for row in cur.fetchall()}
    print(f"[INFO] rows to keep: {len(keep_ids)}")

    # ② 删除不在 keep_ids 的行
    cur.execute(f"""
        DELETE FROM results
        WHERE id NOT IN ({','.join('?'*len(keep_ids))})
    """, tuple(keep_ids))
    deleted = cur.rowcount
    conn.commit(); conn.close()
    print(f"[INFO] duplicates removed: {deleted}")

if __name__ == "__main__":
    dedup_results(RESULT_DB)