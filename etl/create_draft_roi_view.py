import sqlite3

# Connect to the fantasy football database
conn = sqlite3.connect("/Users/arankirwan/fantasy-football-data/db/fantasy_football.db")
cur = conn.cursor()

# Drop the view if it exists
cur.execute("DROP VIEW IF EXISTS draft_roi_view;")

# Create the draft ROI view
cur.execute("""
CREATE VIEW draft_roi_view AS
SELECT 
    dr.season_year,
    t.team_id,
    t.owner_name,
    dr.round,
    dr.pick,
    p.player_id,
    p.name AS player_name,
    p.position,
    p.pro_team,
    COALESCE(bs.total_points, 0) AS total_points,
    s.final_rank,
    CASE WHEN dr.round = 1 THEN 1 ELSE 0 END AS is_keeper
FROM draft_results dr
JOIN players p ON dr.player_id = p.player_id
JOIN teams t ON dr.team_id = t.team_id
LEFT JOIN (
    SELECT 
        player_id,
        season_year,
        SUM(points) AS total_points
    FROM box_scores
    GROUP BY player_id, season_year
) bs ON bs.player_id = dr.player_id AND bs.season_year = dr.season_year
LEFT JOIN standings s ON s.season_year = dr.season_year AND s.team_id = dr.team_id
GROUP BY 
    dr.season_year, t.team_id, t.owner_name, dr.round, dr.pick,
    p.player_id, p.name, p.position, p.pro_team, bs.total_points, s.final_rank, is_keeper
""")

print("✅ Created draft_roi_view")

conn.commit()
conn.close()
