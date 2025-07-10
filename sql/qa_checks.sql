-- QA CHECKS FOR FANTASY FOOTBALL DATABASE

-- 1. Season Coverage
SELECT DISTINCT 'teams' AS table_name, season_year FROM teams;
SELECT DISTINCT 'rosters' AS table_name, season_year FROM rosters;
SELECT DISTINCT 'matchups' AS table_name, season_year FROM matchups;
SELECT DISTINCT 'standings' AS table_name, season_year FROM standings;
SELECT DISTINCT 'draft_results' AS table_name, season_year FROM draft_results;

-- 2. Team Count by Season
SELECT season_year, COUNT(DISTINCT team_id) AS team_count
FROM teams
GROUP BY season_year
ORDER BY season_year;

-- 3. Week 1 Roster Sizes
SELECT season_year, COUNT(*) AS week1_roster_size
FROM rosters
WHERE week = 1
GROUP BY season_year
ORDER BY season_year;

-- 4. Player Join Check
SELECT r.season_year, r.team_id, r.player_id
FROM rosters r
LEFT JOIN players p ON r.player_id = p.player_id
WHERE p.name IS NULL
LIMIT 10;

-- 5. Missing Values
SELECT * FROM teams WHERE owner_name IS NULL OR team_name IS NULL;
SELECT * FROM standings WHERE final_rank IS NULL OR wins IS NULL;

-- 6. Duplicate Rosters
SELECT season_year, week, team_id, player_id, COUNT(*) AS count
FROM rosters
GROUP BY season_year, week, team_id, player_id
HAVING count > 1
LIMIT 10;

-- 7. Orphaned Rosters (Team Key Mismatch)
SELECT *
FROM rosters r
LEFT JOIN teams t ON r.team_id = t.team_id AND r.season_year = t.season_year
WHERE t.team_id IS NULL
LIMIT 10;
