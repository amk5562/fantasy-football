import sqlite3
import csv

DB_PATH = "db/fantasy_football.db"
CSV_PATH = "data/rookies_2024_template.csv"

# Load rookie names from CSV
with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rookie_names = set(row["player_name"].strip() for row in reader if row["player_name"].strip())

print(f"🧑‍🎓 Found {len(rookie_names)} rookie names in CSV.")

# Connect to DB and update player records
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

updated_count = 0
for name in rookie_names:
    cursor.execute("""
        UPDATE players
        SET is_rookie = 1
        WHERE LOWER(name) = LOWER(?)
    """, (name,))
    if cursor.rowcount:
        print(f"✅ Updated rookie flag for: {name}")
        updated_count += cursor.rowcount

conn.commit()
conn.close()

print(f"\n🎯 Done. Total rookies updated: {updated_count}")
