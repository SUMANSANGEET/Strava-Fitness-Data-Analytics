"""
build_db.py
Loads the three cleaned CSVs exported by the notebook
(cleaned_daily_master.csv, cleaned_hourly_master.csv, user_segments.csv)
into a SQLite database (bellabeat.db) following schema.sql.

Usage:
    python build_db.py
Produces:
    bellabeat.db  (in the same folder)
"""

import sqlite3
import pandas as pd
from pathlib import Path

HERE = Path(__file__).parent
DB_PATH = HERE / "bellabeat.db"
SCHEMA_PATH = HERE / "schema.sql"

DAILY_CSV = HERE / "cleaned_daily_master.csv"
HOURLY_CSV = HERE / "cleaned_hourly_master.csv"
SEGMENTS_CSV = HERE / "user_segments.csv"


def build():
    # Fresh DB each run
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Create schema
    cur.executescript(SCHEMA_PATH.read_text())

    # 2. Load dim_user
    users = pd.read_csv(SEGMENTS_CSV)
    users.to_sql("dim_user", conn, if_exists="append", index=False)

    # 3. Load fact_daily_activity
    daily = pd.read_csv(DAILY_CSV, parse_dates=["ActivityDate"])
    daily["ActivityDate"] = daily["ActivityDate"].dt.strftime("%Y-%m-%d")
    for col in ("IsWeekend", "ZeroActivityDay", "HasSleepData"):
        daily[col] = daily[col].astype(int)
    daily.to_sql("fact_daily_activity", conn, if_exists="append", index=False)

    # 4. Load fact_hourly_activity
    hourly = pd.read_csv(HOURLY_CSV, parse_dates=["ActivityHour"])
    hourly["ActivityHour"] = hourly["ActivityHour"].dt.strftime("%Y-%m-%d %H:%M:%S")
    hourly.to_sql("fact_hourly_activity", conn, if_exists="append", index=False)

    conn.commit()

    # 5. Sanity check row counts
    for tbl in ("dim_user", "fact_daily_activity", "fact_hourly_activity"):
        n = cur.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"{tbl:24s} -> {n:>6} rows")

    conn.close()
    print(f"\nDatabase built at: {DB_PATH}")


if __name__ == "__main__":
    build()
