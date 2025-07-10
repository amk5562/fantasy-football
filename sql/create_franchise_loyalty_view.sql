CREATE VIEW IF NOT EXISTS franchise_loyalty_view AS
WITH
current_season AS (
    SELECT season_year, franchise_id, player_id
    FROM core_players_view
),
previous_season AS (
    SELECT season_year + 1 AS season_year, franchise_id, player_id
    FROM core_players_view
),
joined AS (
    SELECT
        c.season_year,
        c.franchise_id,
        COUNT(*) AS returning_core_players
    FROM current_season c
    JOIN previous_season p
      ON c.season_year = p.season_year
     AND c.franchise_id = p.franchise_id
     AND c.player_id = p.player_id
    GROUP BY c.season_year, c.franchise_id
),
core_totals AS (
    SELECT
        season_year,
        franchise_id,
        COUNT(*) AS core_total_prev
    FROM core_players_view
    GROUP BY season_year, franchise_id
)
SELECT
    j.season_year,
    j.franchise_id,
    j.returning_core_players,
    c.core_total_prev,
    ROUND(1.0 * j.returning_core_players / c.core_total_prev, 3) AS loyalty_score
FROM joined j
JOIN core_totals c
  ON j.season_year = c.season_year
 AND j.franchise_id = c.franchise_id
ORDER BY j.season_year, j.franchise_id;