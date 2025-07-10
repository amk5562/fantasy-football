

import sqlite3

DB_PATH = "db/fantasy_football.db"

def print_table_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    print(f"📊 {table_name}: {count} rows")

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("🔍 Checking key tables...\n")

    tables = [
        "schedule",
        "teams",
        "playoffs",
        "standings",
        "players",
        "rosters",
        "draft_results"
    ]

    for table in tables:
        try:
            print_table_count(cursor, table)
        except sqlite3.OperationalError as e:
            print(f"⚠️  Error accessing table '{table}': {e}")

    print("\n🧪 Verifying view: schedule_team_view")
    try:
        cursor.execute("SELECT COUNT(*) FROM schedule_team_view;")
        count = cursor.fetchone()[0]
        print(f"✅ schedule_team_view: {count} rows")
    except sqlite3.OperationalError as e:
        print(f"❌ schedule_team_view failed: {e}")

    print("\n🔁 Checking for duplicate rows in schedule...")
    cursor.execute("""
        SELECT season_year, week, team_id, COUNT(*) as count
        FROM schedule
        GROUP BY season_year, week, team_id
        HAVING count > 1;
    """)
    dupes = cursor.fetchall()
    if dupes:
        print(f"⚠️  Found duplicate schedule rows: {dupes}")
    else:
        print("✅ No duplicate schedule rows.")

    conn.close()

if __name__ == "__main__":
    main()