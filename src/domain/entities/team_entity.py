from pydantic import BaseModel

class TeamEntity(BaseModel):
    teamId: int
    abbreviation: str
    location: str
    name: str