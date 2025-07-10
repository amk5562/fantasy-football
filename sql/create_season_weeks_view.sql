CREATE VIEW season_weeks_view AS
SELECT
  season_year,
  MAX(week) AS total_weeks
FROM rosters
GROUP BY season_year;
