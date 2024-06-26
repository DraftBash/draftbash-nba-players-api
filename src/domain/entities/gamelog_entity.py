from pydantic import BaseModel

class GamelogEntity(BaseModel):
    gameId: int
    season: int
    date: str
    playerId: int
    playerTeamId: int
    isHomeGame: bool
    opposingTeamId: int
    playerTeamScore: int
    opposingTeamScore: int
    position: str
    isStarter: bool
    minutes: float
    points: int
    fieldGoalsMade: int
    fieldGoalsAttempted: int
    threesMade: int
    threesAttempted: int
    freeThrowsMade: int
    freeThrowsAttempted: int
    reboundsOffensive: int
    reboundsDefensive: int
    reboundsTotal: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    fouls: int
    plusMinus: int
