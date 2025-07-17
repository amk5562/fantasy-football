import sqlite3
from espn_api.football import League
from etl.utils import get_valid_seasons

# CONFIG
LEAGUE_ID = 1206951
SWID = '{BE77C299-A100-456A-9A58-03DFD0A2086B}'
ESPN_S2 = 'AEC16mIZMNA9bMEJH9uBtCqDR6xwbvv8HOxwN%2F5cW%2BwGBgwyYtfhsOwRA9UlzozruQzSxUPsTqMjvNZaPpsiRqcb5kgS4iRWwjF%2FcnGXfidQQUN0eF8jruhwzyQLiE2IWkcPhMpNn4S9mee%2BCRCDyvdCejjEGTK%2BYNsT7GAx5kiwY%2FCfxt73V8NTHQ1qqDTL23bsrwg8ApHRyFTj03DbMvyq5Z4GOJ8D6FgQsLMClkI5VvRJoek0HQiPWJ4S2a8aeY%2BXo1gRh1a3yybzNbyK319n'

# Connect to SQLite DB
conn = sqlite3.connect("db/fantasy_football.db")
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    name TEXT,
    position TEXT,
    pro_team TEXT,
    is_rookie INTEGER DEFAULT 0
)
""")

# Extract unique players across all seasons
seen = set()
total_inserted = 0
for year in get_valid_seasons():
    print(f"🔄 Loading players for season {year}")
    league = League(league_id=LEAGUE_ID, year=year, swid=SWID, espn_s2=ESPN_S2)
    year_count = 0
    for team in league.teams:
        if not team.roster:
            continue
        for player in team.roster:
            if player.playerId not in seen:
                seen.add(player.playerId)
                cur.execute("""
INSERT OR IGNORE INTO players (player_id, name, position, pro_team, is_rookie)
VALUES (?, ?, ?, ?, ?)
""", (
    player.playerId,
    player.name,
    player.position,
    player.proTeam,
    int(getattr(player, 'rookie', False))
))
                cur.execute("""
UPDATE players
SET pro_team = ?
WHERE player_id = ?
""", (
    player.proTeam,
    player.playerId
))
                year_count += 1
            player_info = {
    "player_id": player.playerId,
    "name": player.name,
    "position": player.position,
    "pro_team": player.proTeam,
    "is_rookie": int(getattr(player, 'rookie', False))
}
    print(f"✅ Inserted {year_count} new players for season {year}")
    total_inserted += year_count

# Finalize
conn.commit()
conn.close()
print(f"✅ Loaded {total_inserted} unique players into 'players' table.")
