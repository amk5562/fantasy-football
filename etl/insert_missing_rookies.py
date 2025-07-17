import sqlite3
import pandas as pd

# Load rookie data from the CSV
rookies_df = pd.read_csv("data/rookies_2024_template.csv")
print(rookies_df.columns)

rookies_df["name"] = rookies_df["player_name"].str.strip()
rookies_df["position"] = rookies_df["position"]

# Open DB connection
conn = sqlite3.connect("db/fantasy_football.db")
cursor = conn.cursor()

inserted_count = 0

for _, row in rookies_df.iterrows():
    name = row["name"]
    pro_team = row["pro_team"]
    position = row["position"]
    player_id = f"ROOKIE_{name.lower().replace(' ', '_')}"

    # Check if player already exists
    cursor.execute("SELECT position, pro_team FROM players WHERE player_id = ?", (player_id,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("""
            UPDATE players
            SET position = COALESCE(NULLIF(position, ''), ?),
                pro_team = COALESCE(NULLIF(pro_team, ''), ?)
            WHERE player_id = ?
        """, (position, pro_team, player_id))
        continue

    # Insert rookie player
    cursor.execute("""
        INSERT INTO players (player_id, name, position, pro_team, is_rookie)
        VALUES (?, ?, ?, ?, 1)
    """, (player_id, name, position, pro_team))
    inserted_count += 1
    print(f"✅ Inserted: {name} ({player_id})")

conn.commit()
conn.close()

print(f"\n🧠 Done. Inserted {inserted_count} new rookies.")