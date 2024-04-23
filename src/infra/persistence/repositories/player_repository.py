from infra.persistence.database import players_collection
from domain.entities import PlayerEntity
from interfaces.repositories import IPlayerRepository


class PlayerRepository(IPlayerRepository):
    """
    Repository for NBA players
    """

    def upsert(self, player: PlayerEntity) -> None:
        """
        Upsert an NBA player
        
        :param player PlayerEntity: The player entity to upsert
        """

        # Define the fields to exclude from updates
        exclude_fields = ["recentNews", "fantasyOutlook", "currentWeekProjections"]

        # Create the document with all fields
        player_document = dict(player)

        # Remove the excluded fields if the player already exists.
        # This is to prevent overwriting the excluded fields with empty values.
        if players_collection.find_one({"playerId": player.playerId}):
            for field in exclude_fields:
                player_document.pop(field, None)

        # Upsert the player into the MongoDB database
        players_collection.update_one(
            {"playerId": player.playerId},
            {"$set": player_document},
            upsert=True,
        )