# tests/test_data_load.py

import sqlite3
from etl.utils import get_valid_seasons
valid_seasons = get_valid_seasons()
print(f"🧪 utils module loaded, valid seasons: {valid_seasons}")

DB_PATH = "db/fantasy_football.db"

# Tables to test
TABLES = [
    "seasons",
    "teams",
    "players",
    "rosters",
    "matchups",
    "schedules",
    "playoffs",
    "draft_results",
    "standings"
]

def test_table_counts(cursor):
    print("🔍 Row counts:")
    for table in TABLES:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table:<16}: {count} rows")

def test_sample_rows(cursor):
    print("\n📌 Sample rows:")
    for table in TABLES:
        cursor.execute(f"SELECT * FROM {table} LIMIT 1")
        row = cursor.fetchone()
        print(f"  {table:<16}: {row}")

if __name__ == "__main__":
    print(f"🧪 Valid seasons from utils: {valid_seasons}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    test_table_counts(cursor)
    test_sample_rows(cursor)

    conn.close()
