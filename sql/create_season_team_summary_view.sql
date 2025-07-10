CREATE VIEW season_team_summary_view AS
SELECT
    t.season_year,
    t.team_id,
    t.owner_name,
    t.team_name,
    s.final_rank,
    s.wins,
    s.losses,
    s.ties,
    s.points_for,
    s.points_against
FROM teams t
JOIN standings s
  ON t.team_id = s.team_id
  AND t.season_year = s.season_year;