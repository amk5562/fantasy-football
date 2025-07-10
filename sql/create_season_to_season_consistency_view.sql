CREATE VIEW IF NOT EXISTS season_to_season_consistency_view AS
WITH paired_seasons AS (
  SELECT 
    w1.season_year AS season1,
    w2.season_year AS season2,
    w1.team_id,
    w1.owner_name,
    w1.team_name,
    COUNT(DISTINCT w1.player_id) AS season1_count,
    COUNT(DISTINCT w2.player_id) AS season2_count,
    COUNT(DISTINCT CASE WHEN w1.player_id = w2.player_id THEN w1.player_id END) AS common_players
  FROM week1_roster_view w1
  JOIN week1_roster_view w2
    ON w1.team_id = w2.team_id
   AND w2.season_year = w1.season_year + 1
  WHERE w1.season_year BETWEEN 2020 AND 2023
    AND w2.season_year BETWEEN 2021 AND 2024
  GROUP BY w1.team_id, w1.season_year, w1.owner_name, w1.team_name, w2.season_year
)
SELECT
  season1,
  season2,
  team_id,
  owner_name,
  team_name,
  common_players,
  season1_count,
  season2_count,
  ROUND(common_players * 1.0 / NULLIF(season1_count + season2_count - common_players, 0), 3) AS jaccard_score
FROM paired_seasons;
