DROP VIEW IF EXISTS draft_results_view;

CREATE VIEW draft_results_view AS
SELECT
    d.season_year,
    d.round,
    d.pick,
    d.team_id,
    t.team_name AS team_name,
    d.player_id,
    p.name AS player_name,
    p.position,
    p.team AS nfl_team
FROM draft_results d
LEFT JOIN teams t ON d.team_id = t.team_id AND d.season_year = t.season_year
LEFT JOIN players p ON d.player_id = p.player_id;
