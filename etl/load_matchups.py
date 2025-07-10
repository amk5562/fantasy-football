import sqlite3
from espn_api.football import League
from etl.utils import get_valid_seasons

# CONFIG
LEAGUE_ID = 1206951
SWID = '{BE77C299-A100-456A-9A58-03DFD0A2086B}'
ESPN_S2 = 'AEC16mIZMNA9bMEJH9uBtCqDR6xwbvv8HOxwN%2F5cW%2BwGBgwyYtfhsOwRA9UlzozruQzSxUPsTqMjvNZaPpsiRqcb5kgS4iRWwjF%2FcnGXfidQQUN0eF8jruhwzyQLiE2IWkcPhMpNn4S9mee%2BCRCDyvdCejjEGTK%2BYNsT7GAx5kiwY%2FCfxt73V8NTHQ1qqDTL23bsrwg8ApHRyFTj03DbMvyq5Z4GOJ8D6FgQsLMClkI5VvRJoek0HQiPWJ4S2a8aeY%2BXo1gRh1a3yybzNbyK319n'

for YEAR in get_valid_seasons():
    # Connect to ESPN API
    league = League(league_id=LEAGUE_ID, year=YEAR, swid=SWID, espn_s2=ESPN_S2)

    # Connect to SQLite DB
    conn = sqlite3.connect("db/fantasy_football.db")
    cur = conn.cursor()

    # Loop over all weeks (including playoffs)
    for week in range(1, 18):
        try:
            matchups = league.box_scores(week)
        except KeyError as e:
            print(f"⚠️  Skipping week {week} in {YEAR} due to missing data: {e}")
            continue

        for i, matchup in enumerate(matchups):
            if isinstance(matchup.away_team, int) or isinstance(matchup.home_team, int):
                continue  # Skip matchups with missing data (bye weeks)

            home_id = matchup.home_team.team_id
            away_id = matchup.away_team.team_id
            home_score = matchup.home_score
            away_score = matchup.away_score
            is_playoff = week > 14

            # Determine result
            home_result = "WIN" if home_score > away_score else "LOSS" if home_score < away_score else "TIE"
            away_result = "WIN" if away_score > home_score else "LOSS" if away_score < home_score else "TIE"

            # Insert home team record
            cur.execute("""
                INSERT OR REPLACE INTO matchups (
                    season_year, week, matchup_id, team_id, opponent_id, team_score, opponent_score, result, is_playoff
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                YEAR, week, i, home_id, away_id, home_score, away_score, home_result, is_playoff
            ))

            # Insert away team record
            cur.execute("""
                INSERT OR REPLACE INTO matchups (
                    season_year, week, matchup_id, team_id, opponent_id, team_score, opponent_score, result, is_playoff
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                YEAR, week, i, away_id, home_id, away_score, home_score, away_result, is_playoff
            ))

    # Finalize
    conn.commit()
    conn.close()
    print(f"✅ Loaded matchups for season {YEAR}.")
