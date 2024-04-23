from datetime import datetime, timedelta
import time
import requests
from domain.entities import GamelogEntity


class GamelogsFetcher:
    """
    Fetches NBA player gamelogs according to the given game_ids.

    :param get_recent_game_ids: Gets the game_ids over the last 10 days
    :param get_season_game_ids: Gets the game_ids for a given season.
    :param execute: Fetches NBA player gamelogs according to the given game_ids.
    """

    def __init__(self):
        # These headers are needed to access the NBA API
        self._nba_api_headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "x-nba-stats-token": "true",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "x-nba-stats-origin": "stats",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Referer": "https://stats.nba.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def get_recent_game_ids(self) -> list[int]:
        """
        Gets the game_ids over the last 10 days

        :return: A list of game_ids for the last 10 days.
        :rtype: list[int]
        """

        # Get the current date and the date 10 days ago
        current_date = datetime.now().strftime("%Y-%m-%d")
        date_ten_days_ago = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

        current_season = datetime.now().year
        if datetime.now().month >= 10:
            current_season = current_season + 1

        # Get the current week's schedule
        game_ids_endpoint = (
            f"https://stats.nba.com/stats/leaguegamefinder?LeagueID=00&Season={current_season-1}-{str(current_season)[2:]}"
        )
        game_ids_response = requests.get(game_ids_endpoint, headers=self._nba_api_headers)

        game_ids = []
        for game in game_ids_response.json()["resultSets"][0]["rowSet"]:
            if game[5] >= date_ten_days_ago and game[5] < current_date:
                game_ids.append(game[4])
        return list(set(game_ids))

    def get_season_game_ids(self, season: int) -> list[int]:
        """
        Gets the game_ids for a given season.

        :param season int: The season for which to get the game_ids, i.e. 2024 for the 2023-24 season.
        :return: A list of game_ids for the given season.
        :rtype: list[int]
        """

        # Get the game_ids for the given season
        game_ids_endpoint = (
            "https://stats.nba.com/stats/leaguegamefinder?LeagueID=00&Season="
            + f"{season-1}-{str(season)[2:]}&SeasonType=Regular Season"
        )
        game_ids_response = requests.get(game_ids_endpoint, headers=self._nba_api_headers)
        game_ids = list(set([game[4] for game in game_ids_response.json()["resultSets"][0]["rowSet"]]))
        return game_ids

    def get_new_gamelogs(self, game_ids: list[int]) -> list[GamelogEntity]:
        """
        Fetches NBA player gamelogs according to the given game_ids.

        :param game_ids list[int]: A list of game_ids for which to fetch gamelogs.
        :return: A list of gamelog entities for each given game_id
        :rtype: list[GamelogEntity]
        """

        # Gets player data, i.e. position, from Sleeper's API
        sleeper_api_players_response = requests.get("https://api.sleeper.app/v1/players/nba")
        sleeper_api_players = sleeper_api_players_response.json()

        # Get the gamelogs for each player in each game in the given game_ids
        gamelogs = []
        for game_id in game_ids:
            try:
                # Get the game data from the NBA API
                NBA_API_GAMES_ENDPOINT = f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{game_id}.json"
                game_response = requests.get(NBA_API_GAMES_ENDPOINT)
                game = game_response.json()["game"]

                # Get the UTC date of the game
                game_date = game["gameTimeUTC"].split("T")[0]
                season = int(game_date.split("-")[0])
                month_number = int(game_date.split("-")[1])
                if month_number >= 1 and month_number < 10:
                    season -= 1

                # Get home team players and team id
                home_team = game["homeTeam"]
                home_team_id = home_team["teamId"]
                home_players = home_team["players"]

                # Get away team players and team id
                away_team = game["awayTeam"]
                away_team_id = away_team["teamId"]
                away_players = away_team["players"]

                # Get the gamelogs for the home players
                for home_player in home_players:
                    stats = home_player["statistics"]
                    position = "NaN"  # Position the player plays, i.e. powerforward, shootingguard, etc
                    minutes = float(stats["minutes"].split("M")[0][2:])
                    seconds = float(stats["minutes"].split("M")[1][:2])
                    minutes_played = minutes + (seconds / 60)

                    # Get the player's position from the player data fetched from Sleeper's API
                    for key, sleeper_api_player in sleeper_api_players.items():
                        if (
                            sleeper_api_player["first_name"] == home_player["firstName"]
                            and sleeper_api_player["last_name"] in home_player["familyName"]
                        ):
                            position = sleeper_api_player["position"]
                            break

                    gamelogs.append(
                        GamelogEntity(
                            gameId=game_id,
                            season=season,
                            date=game_date,
                            playerId=home_player["personId"],
                            playerTeamId=home_team_id,
                            isHomeGame=True,
                            opposingTeamId=away_team_id,
                            playerTeamScore=home_team["score"],
                            opposingTeamScore=away_team["score"],
                            position=position,
                            isStarter=home_player["starter"],
                            minutes=minutes_played,
                            points=stats["points"],
                            assists=stats["assists"],
                            reboundsTotal=stats["reboundsTotal"],
                            reboundsDefensive=stats["reboundsDefensive"],
                            reboundsOffensive=stats["reboundsOffensive"],
                            steals=stats["steals"],
                            blocks=stats["blocks"],
                            turnovers=stats["turnovers"],
                            fieldGoalsAttempted=stats["fieldGoalsAttempted"],
                            fieldGoalsMade=stats["fieldGoalsMade"],
                            freeThrowsAttempted=stats["freeThrowsAttempted"],
                            freeThrowsMade=stats["freeThrowsMade"],
                            threesAttempted=stats["threePointersAttempted"],
                            threesMade=stats["threePointersMade"],
                            plusMinus=stats["plusMinusPoints"],
                            fouls=stats["foulsPersonal"]
                        )
                    )

                # Get the gamelogs for the away players
                for away_player in away_players:
                    stats = away_player["statistics"]
                    position = "NaN"
                    minutes = float(stats["minutes"].split("M")[0][2:])
                    seconds = float(stats["minutes"].split("M")[1][:2])
                    minutes_played = minutes + (seconds / 60)

                    # Get the player's position from the player data fetched from Sleeper's API
                    for key, player in sleeper_api_players.items():
                        if (
                            player["first_name"] == away_player["firstName"]
                            and player["last_name"] in away_player["familyName"]
                        ):
                            position = sleeper_api_player["position"]
                            break

                    gamelogs.append(
                        GamelogEntity(
                            gameId=game_id,
                            season=season,
                            date=game_date,
                            playerId=home_player["personId"],
                            playerTeamId=home_team_id,
                            isHomeGame=True,
                            opposingTeamId=away_team_id,
                            playerTeamScore=home_team["score"],
                            opposingTeamScore=away_team["score"],
                            position=position,
                            isStarter=home_player["starter"],
                            minutes=minutes_played,
                            points=stats["points"],
                            assists=stats["assists"],
                            reboundsTotal=stats["reboundsTotal"],
                            reboundsDefensive=stats["reboundsDefensive"],
                            reboundsOffensive=stats["reboundsOffensive"],
                            steals=stats["steals"],
                            blocks=stats["blocks"],
                            turnovers=stats["turnovers"],
                            fieldGoalsAttempted=stats["fieldGoalsAttempted"],
                            fieldGoalsMade=stats["fieldGoalsMade"],
                            freeThrowsAttempted=stats["freeThrowsAttempted"],
                            freeThrowsMade=stats["freeThrowsMade"],
                            threesAttempted=stats["threePointersAttempted"],
                            threesMade=stats["threePointersMade"],
                            plusMinus=stats["plusMinusPoints"],
                            fouls=stats["foulsPersonal"]
                        )
                    )
            except Exception as e:
                raise Exception(f"Error fetching gamelogs for game_id: {game_id}. Error: {e}")
            finally:
                # Pause for 0.05 seconds before requesting the next gamelogs to avoid overloading the NBA API.
                time.sleep(0.05)

        return gamelogs