import sqlite3
from espn_api.football import League
from config.credentials import LEAGUE_ID, YEAR, SWID, ESPN_S2
from etl.utils import log_etl_success

# Connect to the database
conn = sqlite3.connect("db/fantasy_football.db")
cur = conn.cursor()

# Ensure the table exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        season_year INTEGER,
        transaction_id INTEGER,
        player_id INTEGER,
        team_id INTEGER,
        type TEXT,
        status TEXT,
        timestamp TEXT,
        PRIMARY KEY (season_year, transaction_id, player_id),
        FOREIGN KEY (season_year) REFERENCES seasons(season_year),
        FOREIGN KEY (team_id) REFERENCES teams(team_id),
        FOREIGN KEY (player_id) REFERENCES players(player_id)
    );
""")

# Fetch transactions from ESPN API
league = League(league_id=LEAGUE_ID, year=YEAR, swid=SWID, espn_s2=ESPN_S2)
try:
    transactions = league.transactions()
except Exception as e:
    if str(e) == "No transactions found":
        print("⚠️ No transactions found. Skipping ETL.")
        conn.close()
        exit()
    else:
        raise

# Safeguard: exit gracefully if no transactions are found
if not transactions:
    print("⚠️ No transactions found. Skipping ETL.")
    conn.close()
    exit()

# Load transactions into database
for txn in transactions:
    for player in txn["adds"]:
        cur.execute("""
            INSERT OR IGNORE INTO transactions (
                season_year, transaction_id, player_id, team_id, type, status, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            YEAR,
            txn["transaction_id"],
            player.playerId,
            txn["adds"][player],
            txn["type"],
            txn["status"],
            txn["timestamp"]
        ))

# Commit and close
conn.commit()
conn.close()

log_etl_success("load_transactions")
print("✅ Loaded transactions.")