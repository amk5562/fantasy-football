from espn_api.football import League

# Replace with your actual league info
LEAGUE_ID = 1206951
YEAR = 2024
SWID = '{BE77C299-A100-456A-9A58-03DFD0A2086B}'
ESPN_S2 = 'AEC16mIZMNA9bMEJH9uBtCqDR6xwbvv8HOxwN%2F5cW%2BwGBgwyYtfhsOwRA9UlzozruQzSxUPsTqMjvNZaPpsiRqcb5kgS4iRWwjF%2FcnGXfidQQUN0eF8jruhwzyQLiE2IWkcPhMpNn4S9mee%2BCRCDyvdCejjEGTK%2BYNsT7GAx5kiwY%2FCfxt73V8NTHQ1qqDTL23bsrwg8ApHRyFTj03DbMvyq5Z4GOJ8D6FgQsLMClkI5VvRJoek0HQiPWJ4S2a8aeY%2BXo1gRh1a3yybzNbyK319n'


league = League(league_id=LEAGUE_ID, year=YEAR, swid=SWID, espn_s2=ESPN_S2)

print(vars(league.settings))

print("🏆 TEAMS")
for team in league.teams:
    print({
        "team_id": team.team_id,
        "team_name": team.team_name,
        "owners": ", ".join([owner["firstName"] + " " + owner["lastName"] for owner in team.owners]),
        "wins": team.wins,
        "losses": team.losses,
        "points_for": team.points_for,
        "points_against": team.points_against
    })

print("\n🔍 LEAGUE ATTRIBUTES:")
print(dir(league))

print("\n🔍 TEAM OBJECT FIELDS:")
team = league.teams[0]
for key in team.__dict__:
    print(f"{key}: {getattr(team, key)}")

print("\n🔍 MATCHUP OBJECT FIELDS:")
matchup = league.box_scores(1)[0]
for key in matchup.__dict__:
    print(f"{key}: {getattr(matchup, key)}")

print("\n🔍 BOXPLAYER OBJECT FIELDS:")
player = matchup.home_lineup[0]
for key in player.__dict__:
    print(f"{key}: {getattr(player, key)}")

print("\n📅 MATCHUPS")
for week in range(1, league.settings.reg_season_count + 1):
    scoreboard = league.box_scores(week)
    for matchup in scoreboard:
        print({
            "week": week,
            "team_id": matchup.home_team.team_id,
            "opponent_id": matchup.away_team.team_id,
            "team_score": matchup.home_score,
            "opponent_score": matchup.away_score
        })
