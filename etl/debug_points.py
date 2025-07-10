from espn_api.football import League
import pprint

LEAGUE_ID = 1206951
SWID = '{BE77C299-A100-456A-9A58-03DFD0A2086B}'
ESPN_S2 = 'AEC16mIZMNA9bMEJH9uBtCqDR6xwbvv8HOxwN%2F5cW%2BwGBgwyYtfhsOwRA9UlzozruQzSxUPsTqMjvNZaPpsiRqcb5kgS4iRWwjF%2FcnGXfidQQUN0eF8jruhwzyQLiE2IWkcPhMpNn4S9mee%2BCRCDyvdCejjEGTK%2BYNsT7GAx5kiwY%2FCfxt73V8NTHQ1qqDTL23bsrwg8ApHRyFTj03DbMvyq5Z4GOJ8D6FgQsLMClkI5VvRJoek0HQiPWJ4S2a8aeY%2BXo1gRh1a3yybzNbyK319n'

league = League(league_id=LEAGUE_ID, year=2023, swid=SWID, espn_s2=ESPN_S2)
box_scores = league.box_scores(1)

for matchup in box_scores:
    for team in [matchup.home_team, matchup.away_team]:
        print(f"\n🏈 Team ID: {team.team_id}")
        for player in team.roster:
            print(f"\n🧾 Raw data for {player.name}:")
            week = 1  # You can change this to the desired week
            points = None
            if hasattr(player, 'stats') and isinstance(player.stats, dict):
                if week in player.stats and 'points' in player.stats[week]:
                    points = player.stats[week]['points']
                elif 0 in player.stats and 'points' in player.stats[0]:
                    points = player.stats[0]['points']
            print(f"🧪 Player {player.name} ({player.playerId}) - Slot: {getattr(player, 'slot_position', getattr(player, 'position', 'N/A'))}, Points: {points}")
            pp = pprint.PrettyPrinter(indent=2)
            # pp.pprint(player.__dict__)
            # break  # Only inspect one player per team to limit output
