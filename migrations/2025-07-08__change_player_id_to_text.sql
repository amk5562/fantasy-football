PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

-- Create new table with TEXT player_id
CREATE TABLE draft_results_new (
    season_year INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    player_id TEXT,  -- changed from INTEGER to TEXT
    round INTEGER,
    pick INTEGER,
    PRIMARY KEY (season_year, team_id, round, pick)
);

-- Copy data into new table
INSERT INTO draft_results_new (season_year, team_id, player_id, round, pick)
SELECT season_year, team_id, player_id, round, pick FROM draft_results;

-- Replace old table
DROP TABLE draft_results;

ALTER TABLE draft_results_new RENAME TO draft_results;

COMMIT;

PRAGMA foreign_keys=on;