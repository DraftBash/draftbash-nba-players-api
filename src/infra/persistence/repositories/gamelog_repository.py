from infra.persistence.database import gamelogs_collection
from interfaces.repositories import IGamelogRepository
from domain.entities import GamelogEntity


class GamelogRepository(IGamelogRepository):
    """
    Repository for gamelogs.
    """

    def upsert(self, gamelog: GamelogEntity) -> None:
        """
        Upsert a gamelog

        :param gamelog GamelogEntity: The gamelog entity to upsert.
        """

        # Upsert the gamelog into the MongoDB database
        gamelogs_collection.update_one(
            {"playerId": dict(gamelog)["playerId"], "date": dict(gamelog)["date"]},
            {"$set": dict(gamelog)},
            upsert=True,
        )
