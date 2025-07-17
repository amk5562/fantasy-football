from espn_api.football import League
import sqlite3

# 🔧 CONFIGURE THESE FIRST
LEAGUE_ID = 1206951
SEASON_YEAR = 2023
ESPN_S2 = 'AEC16mIZMNA9bMEJH9uBtCqDR6xwbvv8HOxwN%2F5cW%2BwGBgwyYtfhsOwRA9UlzozruQzSxUPsTqMjvNZaPpsiRqcb5kgS4iRWwjF%2FcnGXfidQQUN0eF8jruhwzyQLiE2IWkcPhMpNn4S9mee%2BCRCDyvdCejjEGTK%2BYNsT7GAx5kiwY%2FCfxt73V8NTHQ1qqDTL23bsrwg8ApHRyFTj03DbMvyq5Z4GOJ8D6FgQsLMClkI5VvRJoek0HQiPWJ4S2a8aeY%2BXo1gRh1a3yybzNbyK319n'
SWID = '{BE77C299-A100-456A-9A58-03DFD0A2086B}'


# 📦 Get local points from SQLite
conn = sqlite3.connect('db/fantasy_football.db')
cur = conn.cursor()

# 🛰️ Pull live data from ESPN
league = League(league_id=LEAGUE_ID, year=SEASON_YEAR, espn_s2=ESPN_S2, swid=SWID)

# 🎯 List of known players to validate (2023 season)
players_to_check = {
    3117251: "Christian McCaffrey",
    3918298: "Josh Allen",
    3043078: "Derrick Henry",
    15847: "Patrick Mahomes"
}

for player_id, name in players_to_check.items():
    # Get local points from DB
    cur.execute("""
        SELECT total_points FROM player_season_points
        WHERE player_id = ? AND season_year = ?;
    """, (player_id, SEASON_YEAR))
    row = cur.fetchone()
    local_points = row[0] if row else 0

    # Pull from ESPN
    espn_points = 0
    for week in range(1, 18):
        box_scores = league.box_scores(week)
        for matchup in box_scores:
            for player in matchup.home_lineup + matchup.away_lineup:
                if player.playerId == player_id:
                    espn_points += player.points

    # Print result
    print(f"\n🧪 {name} (ID: {player_id})")
    print(f"📘 Local DB Points: {local_points}")
    print(f"🛰️ ESPN Points:    {espn_points:.1f}")
    print(f"🧮 Difference:     {espn_points - local_points:.1f}")
