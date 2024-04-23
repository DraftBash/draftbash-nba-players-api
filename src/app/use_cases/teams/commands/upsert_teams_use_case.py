from interfaces.repositories import ITeamRepository
from domain.entities import TeamEntity


class UpsertTeamsUseCase():
    """ This class is responsible for upserting teams into the database
    """

    def __init__(self, team_repository: ITeamRepository):
        self.team_repository = team_repository
    
    def execute(self, teams: list[TeamEntity]) -> None:
        """ This method is responsible for upserting the week's scheduled matchups into the database.
        :param teams: list[Team]
        :returns: None
        """
        
        for team in teams:
            self.team_repository.upsert(team)
