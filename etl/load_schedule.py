from espn_api.football import League
import sqlite3
from config.credentials import LEAGUE_ID, SWID, ESPN_S2
from etl.utils import log_etl_success, get_valid_seasons

# Connect to database
conn = sqlite3.connect("db/fantasy_football.db")
cursor = conn.cursor()

for YEAR in get_valid_seasons():
    print(f"🔄 Loading schedule for season {YEAR}")
    league = League(league_id=LEAGUE_ID, year=YEAR, swid=SWID, espn_s2=ESPN_S2)

    for week in range(1, 18):
        scoreboard = league.scoreboard(week)
        seen_matchups = set()
        for matchup in scoreboard:
            home_id = matchup.home_team.team_id if hasattr(matchup, 'home_team') and matchup.home_team else None
            away_id = matchup.away_team.team_id if hasattr(matchup, 'away_team') and matchup.away_team else None
            if home_id is None or away_id is None:
                continue
            matchup_key = tuple(sorted((home_id, away_id)))
            if matchup_key in seen_matchups:
                continue
            seen_matchups.add(matchup_key)

            # Insert one row for home team
            cursor.execute("""
                INSERT OR REPLACE INTO schedules (season_year, week, team_id, opponent_id)
                VALUES (?, ?, ?, ?)
            """, (YEAR, week, home_id, away_id))

            # Insert one row for away team
            cursor.execute("""
                INSERT OR REPLACE INTO schedules (season_year, week, team_id, opponent_id)
                VALUES (?, ?, ?, ?)
            """, (YEAR, week, away_id, home_id))
    print(f"✅ Loaded schedule for {YEAR}")

# Commit and close
conn.commit()
conn.close()

# Log the success
log_etl_success("load_schedule", "✅ Loaded schedule for all 17 weeks.")

print(f"✅ Loaded schedule for all 17 weeks.")
