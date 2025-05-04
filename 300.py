import sqlite3

DB = "result8.db"
TABLE = "results"
KEY   = "id"        # 排序字段

with sqlite3.connect(DB) as conn:
    cur = conn.cursor()
    cur.execute(f"""
        DELETE FROM {TABLE}
        WHERE {KEY} NOT IN (
            SELECT {KEY} FROM {TABLE}
            ORDER BY {KEY} ASC LIMIT 300
        )
    """)
    conn.commit()