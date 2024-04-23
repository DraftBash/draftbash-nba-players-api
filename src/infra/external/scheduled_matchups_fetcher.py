from domain.entities import ScheduledMatchupEntity
import requests


class ScheduledMatchupsFetcher:
    """This class is responsible for fetching the weekly team schedules
    from the NBA api and returning a list of ScheduleMatchup objects."
    """

    def execute(self) -> list[ScheduledMatchupEntity]:
        """This method is responsible for fetching the weekly team schedules from the NBA API.
        :return: list[TeamSchedule]
        :params: None
        """

        # Get the current week's schedule
        URL = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"
        response = requests.get(URL) # Make request to the NBA schedule API.
        game_dates = response.json()["leagueSchedule"]["gameDates"]
        current_week_schedule = [game_date for game_date in game_dates]

        # Create a list of scheduled matchups for the week
        week_matchups = []
        for game_date in current_week_schedule:
            for game in game_date["games"]:
                scheduled_matchup = ScheduledMatchupEntity(
                    gameId=game["gameId"],
                    dateTimeUTC=game["gameDateTimeUTC"],
                    homeTeamId=game["homeTeam"]["teamId"],
                    awayTeamId=game["awayTeam"]["teamId"],
                )
                week_matchups.append(scheduled_matchup)

        return week_matchups
