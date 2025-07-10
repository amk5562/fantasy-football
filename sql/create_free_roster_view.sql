CREATE VIEW free_roster_view AS
SELECT
  season_year,
  team_id,
  player_id,
  COUNT(DISTINCT week) AS weeks_on_team
FROM rosters
GROUP BY season_year, team_id, player_id;

