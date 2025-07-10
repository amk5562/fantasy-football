-- Table: seasons
CREATE TABLE IF NOT EXISTS seasons (
    season_year INTEGER PRIMARY KEY
);

-- Table: teams
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    season_year INTEGER,
    owner_name TEXT,
    team_name TEXT,
    wins INTEGER,
    losses INTEGER,
    ties INTEGER,
    points_for REAL,
    points_against REAL,
    standing INTEGER,
    FOREIGN KEY (season_year) REFERENCES seasons(season_year)
);

-- Table: players
CREATE TABLE IF NOT EXISTS players (
    player_id TEXT PRIMARY KEY,
    name TEXT,
    position TEXT,
    team TEXT
);

CREATE TABLE IF NOT EXISTS rosters (
    season_year INTEGER,
    team_id INTEGER,
    player_id TEXT,
    week INTEGER,
    slot_position TEXT,
    points REAL,
    projected_points REAL,
    is_starter INTEGER,
    PRIMARY KEY (season_year, team_id, player_id, week),
    FOREIGN KEY (season_year) REFERENCES seasons(season_year),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- Table: matchups
CREATE TABLE IF NOT EXISTS matchups (
    season_year INTEGER,
    week INTEGER,
    matchup_id INTEGER,
    team_id INTEGER,
    opponent_id INTEGER,
    team_score REAL,
    opponent_score REAL,
    result TEXT,
    is_playoff INTEGER,
    PRIMARY KEY (season_year, week, matchup_id, team_id),
    FOREIGN KEY (season_year) REFERENCES seasons(season_year),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (opponent_id) REFERENCES teams(team_id)
);

-- Table: schedule
CREATE TABLE IF NOT EXISTS schedules (
    season_year INTEGER,
    week INTEGER,
    matchup_id INTEGER,
    team_id INTEGER,
    opponent_id INTEGER,
    PRIMARY KEY (season_year, week, matchup_id, team_id),
    FOREIGN KEY (season_year) REFERENCES seasons(season_year),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (opponent_id) REFERENCES teams(team_id)
);

-- Table: playoffs
CREATE TABLE IF NOT EXISTS playoffs (
    season_year INTEGER,
    week INTEGER,
    round TEXT,
    team_id INTEGER,
    opponent_id INTEGER,
    result TEXT,
    PRIMARY KEY (season_year, week, team_id),
    FOREIGN KEY (season_year) REFERENCES seasons(season_year),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (opponent_id) REFERENCES teams(team_id)
);

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
FROM schedules s
LEFT JOIN playoffs p
    ON s.season_year = p.season_year AND s.week = p.week AND s.team_id = p.team_id;

-- Table: draft_results
CREATE TABLE IF NOT EXISTS draft_results (
    season_year INTEGER,
    round INTEGER,
    pick INTEGER,
    pick_number INTEGER,
    team_id INTEGER,
    player_id TEXT,
    PRIMARY KEY (season_year, round, pick_number),
    FOREIGN KEY (season_year) REFERENCES seasons(season_year),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- Table: standings
CREATE TABLE IF NOT EXISTS standings (
    season_year INTEGER,
    team_id INTEGER,
    final_rank INTEGER,
    wins INTEGER,
    losses INTEGER,
    ties INTEGER,
    points_for REAL,
    points_against REAL,
    PRIMARY KEY (season_year, team_id),
    FOREIGN KEY (season_year) REFERENCES seasons(season_year),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);