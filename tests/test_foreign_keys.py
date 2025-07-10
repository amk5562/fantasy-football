import sqlite3

# Connect to the database
conn = sqlite3.connect("db/fantasy_football.db")
cur = conn.cursor()

print("🔎 Checking foreign key consistency...\n")

# Define checks: (description, SQL to find orphaned rows)
checks = [
    ("🧩 Orphaned rosters.team_id", """
        SELECT * FROM rosters
        WHERE team_id NOT IN (SELECT team_id FROM teams)
    """),
    ("🧩 Orphaned rosters.player_id", """
        SELECT * FROM rosters
        WHERE player_id NOT IN (SELECT player_id FROM players)
    """),
    ("🧩 Orphaned rosters.season_year", """
        SELECT * FROM rosters
        WHERE season_year NOT IN (SELECT season_year FROM seasons)
    """),
    ("🧩 Orphaned matchups.team_id", """
        SELECT * FROM matchups
        WHERE team_id NOT IN (SELECT team_id FROM teams)
    """),
    ("🧩 Orphaned matchups.opponent_id", """
        SELECT * FROM matchups
        WHERE opponent_id NOT IN (SELECT team_id FROM teams)
    """),
    ("🧩 Orphaned schedules.team_id", """
        SELECT * FROM schedules
        WHERE team_id NOT IN (SELECT team_id FROM teams)
    """),
    ("🧩 Orphaned draft_results.team_id", """
        SELECT * FROM draft_results
        WHERE team_id NOT IN (SELECT team_id FROM teams)
    """),
    ("🧩 Orphaned draft_results.player_id", """
        SELECT * FROM draft_results
        WHERE player_id NOT IN (SELECT player_id FROM players)
    """),
]

# Run checks
for label, query in checks:
    cur.execute(query)
    rows = cur.fetchall()
    if rows:
        print(f"{label} ❌ Found {len(rows)} orphaned rows")
    else:
        print(f"{label} ✅ OK")

conn.close()
