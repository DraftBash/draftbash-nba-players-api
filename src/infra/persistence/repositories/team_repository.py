from interfaces.repositories import ITeamRepository
from infra.persistence.database import teams_collection
from domain.entities import TeamEntity

class TeamRepository(ITeamRepository):
    """ 
    Repository for NBA teams. 
    """

    def upsert(self, team: TeamEntity) -> None:
        """Upsert an NBA team
        :return: None
        :param team: Team
        """

        teams_collection.update_one(
            {"teamId": dict(team)['teamId']},
            {"$set": dict(team)},
            upsert=True
        )
        
    def get_team(self, team_id: int) -> TeamEntity:
        """ Get an NBA team
        :return: Team
        :param team_id: int
        """

        team = teams_collection.find_one({"teamId": team_id})
        return TeamEntity(**team)