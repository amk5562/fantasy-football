-- View: schedule_team_view
CREATE VIEW IF NOT EXISTS schedule_team_view AS
SELECT
    s.season_year,
    s.week,
    s.team_id,
    s.opponent_id,
    CASE
        WHEN p.team_id IS NOT NULL THEN 1
        ELSE 0
    END AS is_playoff
FROM schedule s
LEFT JOIN playoffs p
    ON s.season_year = p.season_year
    AND s.week = p.week
    AND s.team_id = p.team_id;
