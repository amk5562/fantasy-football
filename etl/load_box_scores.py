import sqlite3
from espn_api.football import League

from config.credentials import LEAGUE_ID, YEAR, SWID, ESPN_S2
from etl.utils import get_valid_season_years

SLOT_MAP = {
    0: "QB",
    1: "TQB",
    2: "RB",
    3: "FLEX",
    4: "WR",
    5: "FLEX",
    6: "TE",
    7: "OP",
    8: "DT",
    9: "DE",
    10: "LB",
    11: "DL",
    12: "CB",
    13: "S",
    14: "DB",
    15: "DP",
    16: "D/ST",
    17: "K",
    18: "P",
    19: "HC",
    20: "Bench",
    21: "IR",
    23: "FLEX",
    24: "EDR",
    25: "Rookie",
    26: "Taxi",
    27: "Suspended"
}

conn = sqlite3.connect("db/fantasy_football.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS box_scores")

cur.execute("""
CREATE TABLE box_scores (
    season_year INTEGER,
    week INTEGER,
    team_id INTEGER,
    player_id INTEGER,
    slot_position TEXT,
    points REAL,
    projected_points REAL,
    is_starter BOOLEAN,
    PRIMARY KEY (season_year, week, team_id, player_id),
    FOREIGN KEY (season_year) REFERENCES seasons(season_year),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
""")

for season_year in get_valid_season_years():
    print(f"🔄 Loading box scores for season {season_year}")
    try:
        league = League(league_id=LEAGUE_ID, year=season_year, swid=SWID, espn_s2=ESPN_S2)
    except Exception as e:
        print(f"⚠️  Skipping {season_year}: League init failed - {e}")
        continue

    for week in range(1, 18):
        try:
            box_scores = league.box_scores(week)
        except Exception as e:
            print(f"⚠️  Skipping week {week} of {season_year}: {e}")
            continue

        for matchup in box_scores:
            for side in ['home', 'away']:
                lineup = getattr(matchup, f"{side}_lineup", [])
                team = getattr(matchup, f"{side}_team", None)
                for box_player in lineup:
                    slot_id = box_player.slot_position
                    slot_position = SLOT_MAP.get(slot_id, "UNKNOWN") if isinstance(slot_id, int) else slot_id
                    points = box_player.points
                    projected_points = box_player.projected_points
                    is_starter = True  # Because we're iterating over lineup directly

                    cur.execute("""
                    INSERT OR REPLACE INTO box_scores (
                        season_year, week, team_id, player_id, slot_position, points, projected_points, is_starter
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        season_year,
                        week,
                        team.team_id if team else None,
                        box_player.playerId,
                        slot_position,
                        points,
                        projected_points,
                        is_starter
                    ))

conn.commit()
conn.close()
print(f"✅ Loaded box scores for all available seasons and 17 weeks.")
