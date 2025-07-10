from espn_api.football import League

LEAGUE_ID = 1206951
YEAR = 2024
SWID = '{BE77C299-A100-456A-9A58-03DFD0A2086B}'
ESPN_S2 = 'AEC16mIZMNA9bMEJH9uBtCqDR6xwbvv8HOxwN%2F5cW%2BwGBgwyYtfhsOwRA9UlzozruQzSxUPsTqMjvNZaPpsiRqcb5kgS4iRWwjF%2FcnGXfidQQUN0eF8jruhwzyQLiE2IWkcPhMpNn4S9mee%2BCRCDyvdCejjEGTK%2BYNsT7GAx5kiwY%2FCfxt73V8NTHQ1qqDTL23bsrwg8ApHRyFTj03DbMvyq5Z4GOJ8D6FgQsLMClkI5VvRJoek0HQiPWJ4S2a8aeY%2BXo1gRh1a3yybzNbyK319n'

league = League(league_id=LEAGUE_ID, year=YEAR, swid=SWID, espn_s2=ESPN_S2)

for week in range(1, 18):
    matchups = league.box_scores(week)
    if matchups:
        print(f"✅ Week {week}: {len(matchups)} matchups found")
    else:
        print(f"❌ Week {week}: No matchups found")