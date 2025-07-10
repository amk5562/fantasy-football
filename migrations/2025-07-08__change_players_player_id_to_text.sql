PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

-- Create new table with TEXT player_id
CREATE TABLE players_new (
    player_id TEXT PRIMARY KEY,  -- changed from INTEGER to TEXT
    name TEXT,
    position TEXT,
    team TEXT
);

-- Copy data into new table
INSERT INTO players_new (player_id, name, position, team)
SELECT player_id, name, position, team FROM players;

-- Replace old table
DROP TABLE players;

ALTER TABLE players_new RENAME TO players;

COMMIT;

PRAGMA foreign_keys=on;
