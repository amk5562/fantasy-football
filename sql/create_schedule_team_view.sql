CREATE VIEW schedule_team_view AS
SELECT
    s.season_year,
    s.week,
    s.team_id,
    t1.team_name AS team_name,
    s.opponent_id,
    t2.team_name AS opponent_name,
    CASE
        WHEN p.week IS NOT NULL THEN 1
        ELSE 0
    END AS is_playoff
FROM schedules s
LEFT JOIN teams t1
    ON s.season_year = t1.season_year AND s.team_id = t1.team_id
LEFT JOIN teams t2
    ON s.season_year = t2.season_year AND s.opponent_id = t2.team_id
LEFT JOIN playoffs p
    ON s.season_year = p.season_year AND s.week = p.week;