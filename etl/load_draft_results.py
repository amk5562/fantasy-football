import sqlite3
from espn_api.football import League
from config.credentials import LEAGUE_ID, YEAR, SWID, ESPN_S2
from etl.utils import log_etl_success
from etl.utils import get_valid_season_years as get_valid_seasons
import re
import difflib

def normalize_name(name):
    name = name.lower()
    name = re.sub(r"[^a-z\s]", "", name)  # remove punctuation
    name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", name)  # remove suffixes
    name = re.sub(r"\s+", " ", name).strip()
    return name

# NOTE: Before running this script, make sure `players.player_id` is TEXT to avoid datatype mismatch with synthetic IDs.
# Connect to database
conn = sqlite3.connect("db/fantasy_football.db")
cur = conn.cursor()

for year in get_valid_seasons():
    try:
        print(f"🔄 Loading draft results for season {year}")
        league = League(league_id=LEAGUE_ID, year=year, swid=SWID, espn_s2=ESPN_S2)
        if not league.draft:
            print(f"⚠️  No draft data for {year}")
            continue

        cur.execute("DELETE FROM draft_results WHERE season_year = ?", (year,))
        for pick in league.draft:
            player = league.player_map.get(getattr(pick, 'playerId', None), None)
            player_name = getattr(pick, 'playerName', None)

            if not player and not player_name:
                print(f"⚠️  Skipping pick due to missing player data: {pick}")
                try:
                    print(f"🧵 RAW PICK DEBUG: {vars(pick)}")
                except TypeError:
                    print(f"⚠️  Cannot inspect pick with vars(): {pick} (type: {type(pick)})")
                continue

            if player and not isinstance(player, str):
                try:
                    print(f"🧍‍♂️ Raw Player Object: {vars(player)}")
                except TypeError:
                    print(f"⚠️  Cannot inspect player with vars(): {player} (type: {type(player)})")
            elif isinstance(player, str):
                print(f"🧍‍♂️ Player as string: {player}")

            name = getattr(player, 'name', None) if not isinstance(player, str) else player
            name = name or player_name
            name = name.strip()

            player_id = None
            position = None
            if not isinstance(player, str):
                player_id = getattr(player, 'playerId', None)
                position = getattr(player, 'position', None)

            # Fallback: try fuzzy match using player name if player_id is missing or player is a string
            if player_id is None and name:
                # Attempt fuzzy match using difflib if exact match fails
                cur.execute("SELECT name, player_id, position FROM players")
                all_players = cur.fetchall()
                player_map = {normalize_name(row[0]): {"name": row[0], "player_id": row[1], "position": row[2]} for row in all_players}
                norm_name = normalize_name(name)
                matches = difflib.get_close_matches(norm_name, list(player_map.keys()), n=1, cutoff=0.9)
                if matches:
                    match_norm_name = matches[0]
                    matched = player_map[match_norm_name]
                    player_id = matched["player_id"]
                    name = matched["name"]
                    position = matched["position"]
                    print(f"🔍 Fuzzy match for '{norm_name}' → '{name}'")
                    if not player_id:
                        print(f"⚠️  Fuzzy match found but player_id missing for '{name}'")
                        with open("etl/unmatched_players.log", "a") as log_file:
                            log_file.write(f"{year},{pick.round_num},{pick.round_pick},{name}\n")
                        continue
                else:
                    # No fuzzy match found, insert synthetic free agent record with sanitized ID
                    synthetic_id = f"FA_{re.sub(r'[^a-z0-9_]', '', normalize_name(name).replace(' ', '_'))[:28]}"
                    player_id = synthetic_id[:32]  # ensure max 32 characters
                    position = "UNK"
                    print(f"⚠️  No match found. Using synthetic ID: {player_id} for '{name}'")

                    with open("etl/unmatched_players.log", "a") as log_file:
                        log_file.write(f"{year},{pick.round_num},{pick.round_pick},{name}\n")

                    cur.execute("""
                        INSERT OR IGNORE INTO players (player_id, name, position)
                        VALUES (?, ?, ?)
                    """, (
                        player_id,
                        name,
                        position
                    ))

            try:
                # Explicit type conversion before insert
                season_year = int(year)
                team_id = int(pick.team.team_id)
                round_num = int(pick.round_num)
                pick_num = int(pick.round_pick)
                player_id_db = str(player_id).strip()[:32] if player_id else "FA-unknown"
                print(f"📦 Inserting: year={season_year}, team_id={team_id}, player_id={player_id_db} (type={type(player_id_db)}), round={round_num}, pick={pick_num}")
                # Pull fantasy points (basic version — replace with actual logic if needed)
                points = getattr(player, 'total_points', None)
                if points is None:
                    points = 0.0

                cur.execute("""
                    INSERT OR REPLACE INTO draft_results (
                        season_year, team_id, player_id, round, pick, points
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    int(season_year),
                    int(team_id),
                    str(player_id_db),
                    int(round_num),
                    int(pick_num),
                    float(points)
                ))

                if player_id_db is not None:
                    cur.execute("""
                        INSERT OR IGNORE INTO players (player_id, name, position)
                        VALUES (?, ?, ?)
                    """, (
                        player_id_db,
                        name,
                        position
                    ))
                else:
                    print(f"⚠️  Draft pick inserted with no player_id: {name} (Round {pick.round_num}, Pick {pick.round_pick})")
            except Exception as attr_err:
                print(f"⚠️  Insert failed for pick: {attr_err}")
                continue
        log_etl_success("load_draft_results.py", f"✅ Loaded {len(league.draft)} draft picks for season {year}.")
    except Exception as e:
        print(f"❌ Skipping {year} due to error: {e}")

conn.commit()

# Create a view to enrich draft results with player and team metadata.
cur.execute("""
    CREATE VIEW IF NOT EXISTS draft_results_view AS
    SELECT 
        d.season_year,
        d.team_id,
        t.team_name,
        t.owner_name,
        t.franchise_id,
        d.round,
        d.pick,
        d.player_id,
        p.name AS player_name,
        p.position
    FROM draft_results d
    LEFT JOIN players p ON d.player_id = p.player_id
    LEFT JOIN teams t ON d.team_id = t.team_id AND d.season_year = t.season_year
""")

conn.close()