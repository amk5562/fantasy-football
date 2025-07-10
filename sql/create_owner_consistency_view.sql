CREATE VIEW IF NOT EXISTS owner_consistency_view AS
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
),
counts AS (
    SELECT
        r.season_year,
        t.franchise_id,
        COUNT(DISTINCT r.player_id) AS total_players,
        COUNT(DISTINCT cp.player_id) AS core_players
    FROM rosters r
    JOIN teams t ON r.season_year = t.season_year AND r.team_id = t.team_id
    LEFT JOIN core_players cp 
        ON r.season_year = cp.season_year AND r.team_id = cp.team_id AND r.player_id = cp.player_id
    GROUP BY r.season_year, t.franchise_id
)
SELECT
    season_year,
    franchise_id,
    total_players,
    core_players,
    ROUND(1.0 * core_players / total_players, 3) AS core_ratio
FROM counts;
