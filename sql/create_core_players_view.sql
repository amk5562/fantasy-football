CREATE VIEW IF NOT EXISTS core_players_view AS
WITH player_weeks AS (
    SELECT
        season_year,
        team_id,
        player_id,
        COUNT(DISTINCT week) AS weeks_played
    FROM rosters
    GROUP BY season_year, team_id, player_id
),
season_weeks AS (
    SELECT
        season_year,
        team_id,
        COUNT(DISTINCT week) AS total_weeks
    FROM rosters
    GROUP BY season_year, team_id
),
core_players AS (
    SELECT
        pw.season_year,
        pw.team_id,
        pw.player_id
    FROM player_weeks pw
    JOIN season_weeks sw
      ON pw.season_year = sw.season_year AND pw.team_id = sw.team_id
    WHERE pw.weeks_played = sw.total_weeks
)
SELECT
    cp.season_year,
    t.franchise_id,
    cp.player_id
FROM core_players cp
JOIN teams t
  ON cp.season_year = t.season_year AND cp.team_id = t.team_id;
