CREATE VIEW core_roster_view AS
SELECT
  r.season_year,
  r.team_id,
  r.player_id,
  COUNT(DISTINCT r.week) AS weeks_on_team,
  sw.total_weeks
FROM rosters r
JOIN season_weeks_view sw
  ON r.season_year = sw.season_year
GROUP BY r.season_year, r.team_id, r.player_id
HAVING COUNT(DISTINCT r.week) = sw.total_weeks;
