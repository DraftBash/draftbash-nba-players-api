from abc import ABC, abstractmethod
from domain.entities import PlayerEntity

class IPlayerRepository(ABC):
    """Interface for Players Repository"""
    
    @abstractmethod
    def upsert(self, player: PlayerEntity) -> dict:
        pass