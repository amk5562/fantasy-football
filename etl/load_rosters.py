import sqlite3
from espn_api.football import League

# CONFIG
LEAGUE_ID = 1206951
SWID = '{BE77C299-A100-456A-9A58-03DFD0A2086B}'
ESPN_S2 = 'AEC16mIZMNA9bMEJH9uBtCqDR6xwbvv8HOxwN%2F5cW%2BwGBgwyYtfhsOwRA9UlzozruQzSxUPsTqMjvNZaPpsiRqcb5kgS4iRWwjF%2FcnGXfidQQUN0eF8jruhwzyQLiE2IWkcPhMpNn4S9mee%2BCRCDyvdCejjEGTK%2BYNsT7GAx5kiwY%2FCfxt73V8NTHQ1qqDTL23bsrwg8ApHRyFTj03DbMvyq5Z4GOJ8D6FgQsLMClkI5VvRJoek0HQiPWJ4S2a8aeY%2BXo1gRh1a3yybzNbyK319n'

SUPPORTED_SEASONS = range(2019, 2025)  # Only load rosters where data is available

import signal

def handle_interrupt(signum, frame):
    raise KeyboardInterrupt()

signal.signal(signal.SIGINT, handle_interrupt)

conn = sqlite3.connect("db/fantasy_football.db")
cur = conn.cursor()

try:
    # Seasons to load
    for year in SUPPORTED_SEASONS:
        print(f"📅 Loading rosters for season {year}")
        print("⏳ Starting weekly loop. Press Ctrl+C to stop...")
        
        # Create table if not exists
        cur.execute("""
        CREATE TABLE IF NOT EXISTS rosters (
            season_year INTEGER,
            week INTEGER,
            team_id INTEGER,
            player_id INTEGER,
            slot_position TEXT,
            is_starter INTEGER,
            points REAL,
            projected_points REAL,
            PRIMARY KEY (season_year, week, team_id, player_id),
            FOREIGN KEY (season_year) REFERENCES seasons(season_year),
            FOREIGN KEY (team_id) REFERENCES teams(team_id),
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
        """)

        insert_count = 0
        failed_weeks = 0  # Track weeks with no box scores or failed inserts
        skipped_players = 0

        try:
            league = League(league_id=LEAGUE_ID, year=year, swid=SWID, espn_s2=ESPN_S2)
            print(f"📡 League loaded for season {year}")
        except Exception as e:
            print(f"❌ Failed to load league for {year}: {e}")
            continue

        for week in range(1, 18):
            try:
                box_scores = league.box_scores(week)
            except Exception as e:
                print(f"⚠️ Skipping week {week} in {year}: {e}")
                continue

            if not box_scores:
                print(f"⚠️ No box scores for week {week} in {year}")
                failed_weeks += 1
                continue

            teams = []
            for matchup in box_scores:
                if hasattr(matchup, "home_team") and hasattr(matchup.home_team, "roster"):
                    teams.append(matchup.home_team)
                if hasattr(matchup, "away_team") and hasattr(matchup.away_team, "roster"):
                    teams.append(matchup.away_team)

            for team in teams:
                print(f"🔍 Processing team {getattr(team, 'team_id', 'unknown')} in week {week}, year {year}")
                if not hasattr(team, "roster"):
                    continue
                for player in team.roster:
                    slot_position = getattr(player, "slot_position", None)
                    if slot_position is None:
                        slot_position = getattr(player, "position", None)
                    points = None
                    projected = None
                    if hasattr(player, "stats"):
                        week_stats = player.stats.get(week)
                        if week_stats:
                            points = week_stats.get("points")
                            projected = week_stats.get("projectedPoints")
                            if points is None or points > 100:  # Filter out likely season totals
                                continue
                        elif 0 in player.stats and "points" in player.stats[0]:
                            points = player.stats[0]["points"]
                    print(f"🧪 Player {player.name} ({player.playerId}) - Slot: {slot_position}, Points: {points}")
                    if slot_position is None or points is None:
                        skipped_players += 1
                        print(f"⚠️ Skipping player {player.name} ({player.playerId}) - slot: {slot_position}, points: {points}, stats: {player.stats}")
                        continue
                    # Determine is_starter
                    is_starter = 0 if slot_position == "Bench" else 1
                    try:
                        cur.execute("""
                            INSERT OR IGNORE INTO rosters (
                                season_year, week, team_id, player_id, slot_position, is_starter, points, projected_points
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            year,
                            week,
                            team.team_id,
                            player.playerId,
                            slot_position,
                            is_starter,
                            points,
                            projected
                        ))
                        insert_count += 1
                    except Exception as e:
                        print(f"❌ Insert error: {e}")

        if insert_count == 0 and failed_weeks >= 3:
            print(f"❌ Too many failed weeks with no data — stopping early for {year}.")
            break

        print(f"ℹ️ Skipped {skipped_players} players for {year}")
        conn.commit()
    conn.close()
    print(f"✅ {year} complete: inserted {insert_count} roster rows.")
except KeyboardInterrupt:
    print("🛑 Stopped manually by user.")
