from etl.utils import get_valid_seasons
import sqlite3
import os
from espn_api.football import League
import json

# Load franchise mapping
with open("etl/franchise_map.json", "r") as f:
    franchise_map = json.load(f)

# CONFIG
LEAGUE_ID = 1206951
SWID = '{BE77C299-A100-456A-9A58-03DFD0A2086B}'
ESPN_S2 = 'AEC16mIZMNA9bMEJH9uBtCqDR6xwbvv8HOxwN%2F5cW%2BwGBgwyYtfhsOwRA9UlzozruQzSxUPsTqMjvNZaPpsiRqcb5kgS4iRWwjF%2FcnGXfidQQUN0eF8jruhwzyQLiE2IWkcPhMpNn4S9mee%2BCRCDyvdCejjEGTK%2BYNsT7GAx5kiwY%2FCfxt73V8NTHQ1qqDTL23bsrwg8ApHRyFTj03DbMvyq5Z4GOJ8D6FgQsLMClkI5VvRJoek0HQiPWJ4S2a8aeY%2BXo1gRh1a3yybzNbyK319n'

# Connect to SQLite DB
db_path = '/Users/arankirwan/fantasy-football-data/db/fantasy_football.db'
print(f"📂 Connecting to DB at: {os.path.abspath(db_path)}")
conn = sqlite3.connect(db_path)
cur = conn.cursor()


season_years = get_valid_seasons()

# Load and insert team data for each season
for year in season_years:
    print(f"🔄 Loading teams for season {year}")
    try:
        league = League(league_id=LEAGUE_ID, year=year, swid=SWID, espn_s2=ESPN_S2)
        print(f"✅ {year} loaded: {len(league.teams)} teams")
    except Exception as e:
        print(f"⚠️ Skipping season {year}: {e}")
        continue
    
    for team in league.teams:
        # Defensive fallback: older seasons may not have structured owner info
        if hasattr(team, "owners") and isinstance(team.owners, list):
            owner_names = ", ".join([
                f"{owner.get('firstName', '').strip()} {owner.get('lastName', '').strip()}"
                for owner in team.owners
            ])
        else:
            owner_names = team.owner  # Fallback to single owner string

        franchise_id = franchise_map.get(owner_names, None)
        print(f"Inserting team {team.team_id} for {year}: {team.team_name} ({owner_names})")
        print(f"📦 Prepared Insert: ({year}, {team.team_id}, {team.team_name}, {owner_names}, {franchise_id}, {team.wins}, {team.losses}, {team.ties}, {team.points_for}, {team.points_against}, {team.standing})")
        cur.execute("""
            INSERT OR REPLACE INTO teams (
                season_year, team_id, team_name, owner_name, franchise_id,
                wins, losses, ties, points_for, points_against, standing
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            year,
            team.team_id,
            team.team_name,
            owner_names,
            franchise_id,
            team.wins,
            team.losses,
            team.ties,
            team.points_for,
            team.points_against,
            team.standing
        ))

# Finalize
conn.commit()
conn.close()
print("✅ Loaded teams for all seasons.")
