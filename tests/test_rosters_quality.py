import sqlite3

# Connect to the database
conn = sqlite3.connect("db/fantasy_football.db")
cur = conn.cursor()

# Check for null slot_position or points
cur.execute("""
    SELECT COUNT(*) FROM rosters
    WHERE slot_position IS NULL OR points IS NULL
""")
nulls = cur.fetchone()[0]

if nulls == 0:
    print("✅ All rosters have valid slot_position and points.")
else:
    print(f"❌ Found {nulls} rosters with missing slot_position or points.")

conn.close()
