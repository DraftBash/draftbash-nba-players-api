from abc import ABC, abstractmethod
from domain.entities import TeamEntity

class ITeamRepository(ABC):
    """ Interface for team repository. """

    @abstractmethod
    def upsert(self, team: TeamEntity) -> None:
        pass
    
    @abstractmethod
    def get_team(self, team_id: int) -> TeamEntity:
        pass