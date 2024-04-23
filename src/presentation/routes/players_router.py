from fastapi import APIRouter, Response
from infra.persistence.repositories import PlayerRepository, TeamRepository
from infra.external import PlayersFetcher
from app.use_cases.players import PlayersUpserterUseCase
from domain.entities.player_entity import PlayerEntity

players_router = APIRouter()  # Router for players

# Dependencies for dependency injection
player_repository = PlayerRepository()
team_repository = TeamRepository()
playersFetcher = PlayersFetcher(team_repository)

@players_router.post("/api/v1/players")
async def upsert_players():
    PlayersUpserterUseCase(player_repository, playersFetcher).execute()
    return Response(status_code=200)
