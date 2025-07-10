CREATE VIEW IF NOT EXISTS week1_roster_view AS
SELECT
  r.season_year,
  r.team_id,
  t.owner_name,
  t.team_name,
  r.player_id,
  p.name AS player_name,
  p.position,
  p.team AS nfl_team
FROM rosters r
INNER JOIN teams t
  ON r.team_id = t.team_id AND r.season_year = t.season_year
INNER JOIN players p
  ON r.player_id = p.player_id
WHERE r.week = 1;