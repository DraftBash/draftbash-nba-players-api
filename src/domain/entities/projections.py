from pydantic import BaseModel

class ProjectionEntity(BaseModel):
    playerId: int
    date: str
    fieldGoalsAttempted: float
    fieldGoalsMade: float
    threesMade: float
    points: float
    steals: float
    blocks: float
    assists: float
    rebounds: float
    turnovers: float
    freeThrowsAttempted: float
    freeThrowsMade: float
