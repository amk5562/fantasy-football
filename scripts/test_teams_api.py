from espn_api.football import League

# 🔐 League credentials
LEAGUE_ID = 1206951
SWID = '{BE77C299-A100-456A-9A58-03DFD0A2086B}'
ESPN_S2 = 'AEC16mIZMNA9bMEJH9uBtCqDR6xwbvv8HOxwN%2F5cW%2BwGBgwyYtfhsOwRA9UlzozruQzSxUPsTqMjvNZaPpsiRqcb5kgS4iRWwjF%2FcnGXfidQQUN0eF8jruhwzyQLiE2IWkcPhMpNn4S9mee%2BCRCDyvdCejjEGTK%2BYNsT7GAx5kiwY%2FCfxt73V8NTHQ1qqDTL23bsrwg8ApHRyFTj03DbMvyq5Z4GOJ8D6FgQsLMClkI5VvRJoek0HQiPWJ4S2a8aeY%2BXo1gRh1a3yybzNbyK319n'

for season in range(2019, 2024 + 1):  # Check from 2019 to 2024
    try:
        print(f"\n🔄 Testing season {season}")
        league = League(league_id=LEAGUE_ID, year=season, espn_s2=ESPN_S2, swid=SWID)
        for team in league.teams:
            print(f"✅ {season} | Team ID: {team.team_id} | Name: {team.team_name} | Owners: {[owner.get('displayName') for owner in team.owners]}")
    except Exception as e:
        print(f"❌ {season} | Failed to fetch teams: {e}")
