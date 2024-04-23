from pydantic import BaseModel

class ScheduledMatchupEntity(BaseModel):
    gameId: int
    dateTimeUTC: str
    homeTeamId: int
    awayTeamId: int