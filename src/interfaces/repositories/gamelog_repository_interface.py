from abc import ABC, abstractmethod
from domain.entities.gamelog_entity import GamelogEntity


class IGamelogRepository(ABC):
    """
    Interface for gamelog repository.
    """

    @abstractmethod
    def upsert(self, gamelog: GamelogEntity) -> dict:
        pass
