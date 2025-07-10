from espn_api.football import League
import sqlite3
from config.credentials import LEAGUE_ID, YEAR, SWID, ESPN_S2
from etl.utils import log_etl_success, get_valid_seasons

# Connect to database
conn = sqlite3.connect("db/fantasy_football.db")
cursor = conn.cursor()

# Create the playoffs table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS playoffs (
    season_year INTEGER,
    week INTEGER,
    round TEXT,
    team_id INTEGER,
    opponent_id INTEGER,
    result TEXT,
    PRIMARY KEY (season_year, week, team_id),
    FOREIGN KEY (season_year) REFERENCES seasons(season_year),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (opponent_id) REFERENCES teams(team_id)
);
""")

for YEAR in get_valid_seasons():
    league = League(league_id=LEAGUE_ID, year=YEAR, swid=SWID, espn_s2=ESPN_S2)

    # Define playoff weeks and rounds
    rounds = {
        15: "Semifinal",
        16: "Final",
        17: "Consolation"
    }

    # Loop through playoff weeks
    for week, round_name in rounds.items():
        scoreboard = league.scoreboard(week)
        for matchup in scoreboard:
            if not matchup.is_playoff:
                continue

            home_id = matchup.home_team.team_id if hasattr(matchup, "home_team") and matchup.home_team else getattr(matchup, "_home_team_id", None)
            away_id = matchup.away_team.team_id if hasattr(matchup, "away_team") and matchup.away_team else getattr(matchup, "_away_team_id", None)
            home_score = getattr(matchup, "home_score", 0)
            away_score = getattr(matchup, "away_score", 0)

            if home_id is None or away_id is None:
                continue  # Skip incomplete matchups

            # Determine results
            home_result = "win" if home_score > away_score else "loss"
            away_result = "win" if away_score > home_score else "loss"

            # Insert both teams' playoff results
            cursor.execute("""
                INSERT OR REPLACE INTO playoffs (season_year, week, round, team_id, opponent_id, result)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (YEAR, week, round_name, home_id, away_id, home_result))

            cursor.execute("""
                INSERT OR REPLACE INTO playoffs (season_year, week, round, team_id, opponent_id, result)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (YEAR, week, round_name, away_id, home_id, away_result))

    print(f"✅ Loaded playoff results for season {YEAR}")

# Commit and close
conn.commit()
conn.close()

# Log and print success
log_etl_success("load_playoffs", "✅ Loaded playoff results for all available seasons.")
print("✅ Loaded playoff results for all available seasons.")
