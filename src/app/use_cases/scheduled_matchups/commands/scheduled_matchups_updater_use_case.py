from domain.entities import ScheduledMatchupEntity
from interfaces.repositories import IScheduledMatchupRepository


class ScheduledMatchupsUpdaterUseCase:
    """
    This class is responsible for updating the week's scheduled matchups into the database.
    
    :param team_schedule_repository IScheduledMatchupRepository: The repository for scheduled matchups.
    """

    def __init__(self, team_schedule_repository: IScheduledMatchupRepository):
        self.team_schedule_repository = team_schedule_repository

    def execute(self, team_schedules: list[ScheduledMatchupEntity]) -> None:
        """This method is responsible for upserting the week's scheduled matchups into the database.
        
        :param team_schedules list[ScheduledMatchup]: A list of scheduled matchups
        """

        for team_schedule in team_schedules:
            self.team_schedule_repository.upsert(team_schedule)