Schema Mapping Preview
# 📊 Schema Mapping: ESPN API → SQLite BI Tables
""
This document maps fields from the `espn-api` Python package to your internal dimensional schema.
""
---
""
## 🏆 Table: teams
""
| ESPN API Field             | SQLite Schema Field     | Notes                          |
|---------------------------|-------------------------|--------------------------------|
| team.team_id              | teams.team_id           | Primary key                   |
| team.team_name            | teams.team_name         | Team name                     |
| team.owners               | teams.owner_name        | Joined from dict values       |
| team.wins                 | teams.wins              | Season wins                   |
| team.losses              | teams.losses            | Season losses                 |
| team.ties                | teams.ties              | Season ties                   |
| team.points_for          | teams.points_for        | Points scored                 |
| team.points_against      | teams.points_against    | Points allowed                |
| team.standing            | teams.standing          | Current league rank           |
| team.logo_url            | (optional)              | Could be added later          |
| league.year              | teams.season_year       | FK to seasons                 |
""
---
""
## 📅 Table: seasons
""
| ESPN API Field             | SQLite Schema Field     | Notes           |
|---------------------------|-------------------------|-----------------|
| league.year               | seasons.season_year     | Primary key     |
""
---
""
## 🔄 Table: matchups
""
| ESPN API Field             | SQLite Schema Field     | Notes                     |
|---------------------------|-------------------------|---------------------------|
| matchup.home_team.team_id | matchups.team_id        | FK to teams               |
| matchup.away_team.team_id | matchups.opponent_id    | FK to teams               |
| matchup.home_score        | matchups.team_score     | Team score                |
| matchup.away_score        | matchups.opponent_score | Opponent score            |
| week                      | matchups.week           | Game week                 |
| league.year               | matchups.season_year    | FK to seasons             |
""
---
""
## 👥 Table: players
""
| ESPN API Field             | SQLite Schema Field     | Notes                |
|---------------------------|-------------------------|----------------------|
| player.playerId           | players.player_id       | Primary key          |
| player.name               | players.name            | Full name            |
"| player.position           | players.position        | e.g., WR, QB, RB     |"
| player.proTeam           | players.team            | NFL team code (e.g. MIA) |
""
---
""
## 📦 Table: rosters
""
| ESPN API Field             | SQLite Schema Field     | Notes                    |
|---------------------------|-------------------------|--------------------------|
| league.year               | rosters.season_year     | FK to seasons            |
| team.team_id              | rosters.team_id         | FK to teams              |
| player.playerId           | rosters.player_id       | FK to players            |
| week                      | rosters.week            | Week number              |
| player.lineupSlot         | rosters.slot_position   | Position played          |
| player.points             | rosters.points          | Fantasy points scored    |
