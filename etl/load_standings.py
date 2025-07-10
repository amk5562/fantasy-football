from espn_api.football import League
import sqlite3
from config.credentials import LEAGUE_ID, SWID, ESPN_S2
from etl.utils import get_valid_seasons, log_etl_success
valid_seasons = get_valid_seasons()
print("🧪 utils module loaded. Valid seasons returned:", valid_seasons)
print("🧪 utils module loaded, valid seasons:", get_valid_seasons())

# Connect to database
conn = sqlite3.connect("db/fantasy_football.db")
cursor = conn.cursor()

# Create the standings table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS standings (
    season_year INTEGER,
    team_id INTEGER,
    final_rank INTEGER,
    wins INTEGER,
    losses INTEGER,
    ties INTEGER,
    points_for REAL,
    points_against REAL,
    PRIMARY KEY (season_year, team_id),
    FOREIGN KEY (season_year) REFERENCES seasons(season_year),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);
""")

for year in valid_seasons:
    print(f"🔄 Loading standings for season {year}")
    league = League(league_id=LEAGUE_ID, year=year, swid=SWID, espn_s2=ESPN_S2)

    for i, team in enumerate(league.standings(), start=1):
        cursor.execute("""
            INSERT OR REPLACE INTO standings (
                season_year, team_id, final_rank, wins, losses, ties, points_for, points_against
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            year,
            team.team_id,
            i,
            team.wins,
            team.losses,
            team.ties,
            team.points_for,
            team.points_against
        ))
    print(f"✅ Loaded standings for season {year}")

# Commit and close
conn.commit()
conn.close()

# Log ETL success
log_etl_success("load_standings", "✅ Loaded standings for all valid seasons.")
print("✅ Loaded standings for all valid seasons.")
