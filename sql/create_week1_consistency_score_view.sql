-- Drop existing view if it exists
DROP VIEW IF EXISTS week1_consistency_score_view;

-- Create the new consistency score view
CREATE VIEW week1_consistency_score_view AS
WITH pairs AS (
  SELECT
    a.owner_name,
    a.team_name,
    a.season_year AS season1,
    b.season_year AS season2,
    COUNT(DISTINCT a.player_id) AS roster1_count,
    COUNT(DISTINCT b.player_id) AS roster2_count,
    COUNT(DISTINCT a.player_id || '-' || b.player_id) 
      FILTER (WHERE a.player_id = b.player_id) AS shared_count
  FROM week1_roster_view a
  JOIN week1_roster_view b
    ON a.owner_name = b.owner_name
   AND a.season_year < b.season_year
  GROUP BY a.owner_name, a.team_name, a.season_year, b.season_year
),
scored_pairs AS (
  SELECT
    owner_name,
    team_name,
    season1,
    season2,
    shared_count * 1.0 / (roster1_count + roster2_count - shared_count) AS jaccard_score
  FROM pairs
)
SELECT
  owner_name,
  team_name,
  ROUND(AVG(jaccard_score), 3) AS avg_consistency_score,
  COUNT(*) AS comparisons
FROM scored_pairs
GROUP BY owner_name, team_name
ORDER BY avg_consistency_score DESC;
